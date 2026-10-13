// Compile with a writable -module-cache-path. macOS AVFoundation, no package dependencies.
import Foundation
import AVFoundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func fail(_ message:String)->Never {
 FileHandle.standardError.write(Data((message+"\n").utf8));exit(1)
}
func load(_ url:URL)->CGImage {
 guard let source=CGImageSourceCreateWithURL(url as CFURL,nil),let img=CGImageSourceCreateImageAtIndex(source,0,nil) else {fail("Cannot load frame: \(url.path)")}
 return img
}
let args=CommandLine.arguments
guard args.count==4,let fps=Int32(args[3]),fps>0,fps<=120 else {fail("Usage: encode-frames FRAMES_DIR OUTPUT.mp4 FPS (1–120)")}
let dir=URL(fileURLWithPath:args[1],isDirectory:true),output=URL(fileURLWithPath:args[2])
guard !FileManager.default.fileExists(atPath:output.path) else {fail("Output exists; choose a new file or explicitly remove your own authorized output.")}
let files: [URL]
do {files=try FileManager.default.contentsOfDirectory(at:dir,includingPropertiesForKeys:nil).filter{$0.lastPathComponent.hasPrefix("frame_") && $0.pathExtension.lowercased()=="png"}.sorted{$0.lastPathComponent<$1.lastPathComponent}}
catch {fail("Cannot list frames: \(error)")}
guard !files.isEmpty else {fail("No frame_000000.png files found")}
for (i,f) in files.enumerated() {guard f.lastPathComponent==String(format:"frame_%06d.png",i) else {fail("Frame numbering must start at zero and be continuous: expected \(i)")}}
let first=load(files[0]),w=first.width,h=first.height
guard w%2==0,h%2==0 else {fail("H.264 dimensions must be even: \(w)x\(h)")}
do {try FileManager.default.createDirectory(at:output.deletingLastPathComponent(),withIntermediateDirectories:true)} catch {fail("Cannot create output directory: \(error)")}
let writer:AVAssetWriter
do {writer=try AVAssetWriter(outputURL:output,fileType:.mp4)} catch {fail("Cannot create writer: \(error)")}
let bitrate=min(30_000_000,max(500_000,w*h*Int(fps)/18))
let input=AVAssetWriterInput(mediaType:.video,outputSettings:[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:w,AVVideoHeightKey:h,AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:bitrate,AVVideoProfileLevelKey:AVVideoProfileLevelH264HighAutoLevel]])
let ad=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:input,sourcePixelBufferAttributes:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32BGRA,kCVPixelBufferWidthKey as String:w,kCVPixelBufferHeightKey as String:h,kCVPixelBufferCGImageCompatibilityKey as String:true,kCVPixelBufferCGBitmapContextCompatibilityKey as String:true])
guard writer.canAdd(input) else {fail("Cannot add video track")};writer.add(input);writer.shouldOptimizeForNetworkUse=true
guard writer.startWriting() else {fail("Cannot start encoding: \(String(describing:writer.error))")};writer.startSession(atSourceTime:.zero)
for (i,url) in files.enumerated() {
 let deadline=Date().addingTimeInterval(30)
 while !input.isReadyForMoreMediaData {
  guard writer.status == .writing,Date()<deadline else {writer.cancelWriting();fail("Encoder failed or stopped accepting frames: \(String(describing:writer.error))")}
  Thread.sleep(forTimeInterval:0.005)
 }
 autoreleasepool {
  let image=load(url)
  guard image.width==w,image.height==h else {writer.cancelWriting();fail("Frame dimensions differ: \(url.lastPathComponent)")}
  var p:CVPixelBuffer?
  guard let pool=ad.pixelBufferPool,CVPixelBufferPoolCreatePixelBuffer(nil,pool,&p)==kCVReturnSuccess,let pixel=p else {fail("Cannot allocate pixel buffer")}
  CVPixelBufferLockBaseAddress(pixel,[])
  guard let ctx=CGContext(data:CVPixelBufferGetBaseAddress(pixel),width:w,height:h,bitsPerComponent:8,bytesPerRow:CVPixelBufferGetBytesPerRow(pixel),space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.noneSkipFirst.rawValue|CGBitmapInfo.byteOrder32Little.rawValue) else {fail("Cannot create frame context")}
  ctx.draw(image,in:CGRect(x:0,y:0,width:w,height:h))
  CVPixelBufferUnlockBaseAddress(pixel,[])
  guard ad.append(pixel,withPresentationTime:CMTime(value:Int64(i),timescale:fps)) else {writer.cancelWriting();fail("Cannot append frame: \(String(describing:writer.error))")}
 }
}
input.markAsFinished();let sem=DispatchSemaphore(value:0);writer.finishWriting{sem.signal()}
guard sem.wait(timeout:.now()+120) == .success,writer.status == .completed else {fail("Encoding did not finish: \(String(describing:writer.error))")}
let asset=AVURLAsset(url:output),gen=AVAssetImageGenerator(asset:asset)
gen.requestedTimeToleranceBefore = .zero;gen.requestedTimeToleranceAfter = .zero
do {
 for i in [0,files.count/2,files.count-1] { _ = try gen.copyCGImage(at:CMTime(value:Int64(i),timescale:fps),actualTime:nil) }
} catch {fail("Encoded but decode verification failed: \(error). Check codec access before assuming media corruption.")}
print("Verified MP4: \(output.path); \(w)x\(h), \(fps)fps, \(Double(files.count)/Double(fps)) seconds, \(files.count) frames")
