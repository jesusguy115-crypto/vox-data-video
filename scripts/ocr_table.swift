import Foundation
import Vision
import ImageIO
func fail(_ s:String)->Never {FileHandle.standardError.write(Data((s+"\n").utf8));exit(1)}
let args=CommandLine.arguments;guard args.count==2 else {fail("Usage: ocr-table TABLE_IMAGE")}
guard let source=CGImageSourceCreateWithURL(URL(fileURLWithPath:args[1]) as CFURL,nil),let image=CGImageSourceCreateImageAtIndex(source,0,nil) else {fail("Cannot read image")}
let request=VNRecognizeTextRequest();request.recognitionLevel = .accurate;request.recognitionLanguages=["zh-Hans","en-US"];request.usesLanguageCorrection=false
try VNImageRequestHandler(cgImage:image).perform([request])
let rows=(request.results ?? []).compactMap {o -> [String:Any]? in guard let c=o.topCandidates(1).first else {return nil};return ["text":c.string,"x":o.boundingBox.midX,"y":1-o.boundingBox.midY,"height":o.boundingBox.height,"confidence":c.confidence]}
let result=try JSONSerialization.data(withJSONObject:rows,options:[.sortedKeys]);FileHandle.standardOutput.write(result)
