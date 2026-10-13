// BGRA frames (top row first), streamed on stdin. No temporary frame images.
import Foundation
import AVFoundation
import CoreVideo
func fail(_ message:String)->Never {FileHandle.standardError.write(Data((message+"\n").utf8));exit(1)}
let a=CommandLine.arguments
guard a.count==6,let w=Int(a[2]),let h=Int(a[3]),let fps=Int32(a[4]),let count=Int(a[5]),w>0,h>0,w%2==0,h%2==0,fps>0,fps<=120,count>0 else {fail("Usage: encode-stream OUTPUT.mp4 WIDTH HEIGHT FPS FRAME_COUNT; stdin=BGRA")}
let out=URL(fileURLWithPath:a[1]);guard !FileManager.default.fileExists(atPath:out.path) else {fail("Output already exists")}
try FileManager.default.createDirectory(at:out.deletingLastPathComponent(),withIntermediateDirectories:true)
let writer=try AVAssetWriter(outputURL:out,fileType:.mp4)
let input=AVAssetWriterInput(mediaType:.video,outputSettings:[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:w,AVVideoHeightKey:h,AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:min(30_000_000,max(500_000,w*h*Int(fps)/18)),AVVideoProfileLevelKey:AVVideoProfileLevelH264HighAutoLevel]])
let adapter=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:input,sourcePixelBufferAttributes:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32BGRA,kCVPixelBufferWidthKey as String:w,kCVPixelBufferHeightKey as String:h])
guard writer.canAdd(input) else {fail("Cannot add track")};writer.add(input);writer.shouldOptimizeForNetworkUse=true
guard writer.startWriting() else {fail("Cannot start encoding: \(String(describing:writer.error))")};writer.startSession(atSourceTime:.zero)
let bytes=w*h*4
func readFrame()->Data {
 var data=Data();data.reserveCapacity(bytes)
 while data.count<bytes {let next=FileHandle.standardInput.readData(ofLength:bytes-data.count);if next.isEmpty {writer.cancelWriting();fail("Incomplete frame: received \(data.count)/\(bytes) bytes")};data.append(next)}
 return data
}
for i in 0..<count {
 let data=readFrame();let deadline=Date().addingTimeInterval(30)
 while !input.isReadyForMoreMediaData {guard writer.status == .writing,Date()<deadline else {writer.cancelWriting();fail("Encoder stalled: \(String(describing:writer.error))")};Thread.sleep(forTimeInterval:0.001)}
 autoreleasepool {
  var raw:CVPixelBuffer?
  guard let pool=adapter.pixelBufferPool,CVPixelBufferPoolCreatePixelBuffer(nil,pool,&raw)==kCVReturnSuccess,let pixel=raw else {fail("Cannot allocate pixel buffer")}
  CVPixelBufferLockBaseAddress(pixel,[])
  let dest=CVPixelBufferGetBaseAddress(pixel)!,stride=CVPixelBufferGetBytesPerRow(pixel)
  data.withUnsafeBytes {source in
   if stride==w*4 {dest.copyMemory(from:source.baseAddress!,byteCount:bytes)}
   else {for row in 0..<h {dest.advanced(by:row*stride).copyMemory(from:source.baseAddress!.advanced(by:row*w*4),byteCount:w*4)}}
  }
  CVPixelBufferUnlockBaseAddress(pixel,[])
  guard adapter.append(pixel,withPresentationTime:CMTime(value:Int64(i),timescale:fps)) else {writer.cancelWriting();fail("Cannot append frame: \(String(describing:writer.error))")}
 }
}
guard FileHandle.standardInput.readData(ofLength:1).isEmpty else {writer.cancelWriting();fail("Unexpected extra frame bytes")}
input.markAsFinished();let done=DispatchSemaphore(value:0);writer.finishWriting{done.signal()}
guard done.wait(timeout:.now()+120) == .success,writer.status == .completed else {fail("Encoding failed: \(String(describing:writer.error))")}
let asset=AVURLAsset(url:out),gen=AVAssetImageGenerator(asset:asset)
gen.requestedTimeToleranceBefore = .zero;gen.requestedTimeToleranceAfter = .zero
for i in [0,count/2,count-1] {_ = try gen.copyCGImage(at:CMTime(value:Int64(i),timescale:fps),actualTime:nil)}
print("Verified MP4: \(w)x\(h), \(fps)fps, \(count) frames")
