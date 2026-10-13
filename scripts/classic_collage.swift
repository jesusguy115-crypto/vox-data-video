import Foundation
import AVFoundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let args=CommandLine.arguments
if args.count != 7 {fatalError("Usage: classic-collage SCENE.json TEXTURES OUTPUT.mp4 WIDTH HEIGHT FPS")}
let raw=try JSONSerialization.jsonObject(with:Data(contentsOf:URL(fileURLWithPath:args[1]))) as! [String:Any]
let outputPath=args[3], outputWidth=Int(args[4])!,outputHeight=Int(args[5])!,outputFPS=Int32(args[6])!
let duration=(raw["duration"] as? Double) ?? 12
let names=raw["players"] as! [String]
let ppp=raw["points_per_possession"] as! [Double]
let efg=raw["efg_percent"] as! [Double]
let titleLines=(raw["title_lines"] as? [String]) ?? ["同样一回合","谁的得分更高？"]
let showEmphasis=(raw["show_emphasis"] as? Bool) ?? false
let focusIndex=ppp.enumerated().max(by:{$0.element < $1.element})!.offset
var fontCache:[String:CTFont]=[:]
var lineCache:[String:CTLine]=[:]
var pieceCache:[String:CGImage]=[:]
let renderStart=Date()
let colors=(raw["palette_colors"] as? [String:[Double]]) ?? [:]
func role(_ name:String,_ fallback:[CGFloat])->[CGFloat] {if let values=colors[name],values.count==3 {return values.map {CGFloat($0)}};return fallback}
let paper=role("paper",[0.95,0.935,0.89]),ink=role("ink",[0.10,0.14,0.15]),muted=role("muted",[0.36,0.39,0.38]),grid=role("grid",[0.78,0.77,0.73]),yellow=role("primary",[0.98,0.82,0.18]),coral=role("secondary",[0.79,0.22,0.14])
let titleInk: [CGFloat] = zip(yellow,[CGFloat(0.2126),0.7152,0.0722]).reduce(CGFloat(0)) {$0+$1.0*$1.1} > 0.61 ? ink:paper
func col(_ rgb:[CGFloat],_ alpha:CGFloat=1)->CGColor {CGColor(colorSpace:CGColorSpaceCreateDeviceRGB(),components:rgb+[alpha])!}
func clamp(_ x:Double)->Double {min(1,max(0,x))}
func smooth(_ x:Double)->Double {let a=clamp(x);return a*a*(3-2*a)}
let textures:[String:CGImage] = Dictionary(uniqueKeysWithValues:["paper","yellow","dark","back"].map { name in
 let src=CGImageSourceCreateWithURL(URL(fileURLWithPath:args[2]+"/"+name+".jpg") as CFURL,nil)!
 return (name,CGImageSourceCreateImageAtIndex(src,0,nil)!)
})
func rough(_ n:Int,_ seed:Int)->CGFloat {
 let value=sin(Double(n*71+seed*153)*1.319)*41241.827
 return CGFloat(value-floor(value))
}
func torn(_ r:CGRect,_ seed:Int,_ amp:CGFloat=8)->CGPath {
 let p=CGMutablePath(),nx=max(4,Int(r.width/13)),ny=max(4,Int(r.height/12))
 p.move(to:CGPoint(x:r.minX,y:r.minY))
 for i in 1...nx {p.addLine(to:CGPoint(x:r.minX+r.width*CGFloat(i)/CGFloat(nx),y:r.minY+(rough(i,seed)-0.5)*amp))}
 for i in 1...ny {p.addLine(to:CGPoint(x:r.maxX+(rough(i,seed+1)-0.5)*amp,y:r.minY+r.height*CGFloat(i)/CGFloat(ny)))}
 for i in 1...nx {p.addLine(to:CGPoint(x:r.maxX-r.width*CGFloat(i)/CGFloat(nx),y:r.maxY+(rough(i,seed+2)-0.5)*amp))}
 for i in 1...ny {p.addLine(to:CGPoint(x:r.minX+(rough(i,seed+3)-0.5)*amp,y:r.maxY-r.height*CGFloat(i)/CGFloat(ny)))}
 p.closeSubpath();return p
}
func draw(_ c:CGContext,_ t:Double,_ fast:Bool) {
 let T=fast ? t*6.10:t
 // Restrained cutout timing: material settles on discrete animation beats.
 let beat=floor(T*12)/12
 c.draw(textures["back"]!,in:CGRect(x:0,y:0,width:1920,height:1080))
 func text(_ value:String,_ x:CGFloat,_ y:CGFloat,_ size:CGFloat,_ rgb:[CGFloat]=ink,_ bold:Bool=false,_ alignment:Int=0,_ alpha:CGFloat=1,_ numeric:Bool=false) {
  let fontName=numeric ? "HelveticaNeue-CondensedBlack":bold ? "PingFangSC-Semibold":"PingFangSC-Regular"
  let fontKey="\(fontName)|\(size)"
  let font=fontCache[fontKey] ?? CTFontCreateWithName(fontName as CFString,size,nil);fontCache[fontKey]=font
  let lineKey="\(value)|\(fontKey)|\(rgb)"
  let l:CTLine
  if let cached=lineCache[lineKey] {l=cached} else {
   let attrs:[NSAttributedString.Key:Any]=[NSAttributedString.Key(kCTFontAttributeName as String):font,NSAttributedString.Key(kCTForegroundColorAttributeName as String):col(rgb)]
   l=CTLineCreateWithAttributedString(NSAttributedString(string:value,attributes:attrs));lineCache[lineKey]=l
  }
  let width=CGFloat(CTLineGetTypographicBounds(l,nil,nil,nil))
  c.saveGState();c.setAlpha(alpha);c.translateBy(x:x-(alignment==1 ? width/2:alignment==2 ? width:0),y:y+CTFontGetAscent(font));c.scaleBy(x:1,y:-1);c.textMatrix = .identity;c.textPosition = .zero;CTLineDraw(l,c);c.restoreGState()
 }
 func line(_ x1:CGFloat,_ y1:CGFloat,_ x2:CGFloat,_ y2:CGFloat,_ rgb:[CGFloat]=grid,_ width:CGFloat=1.5,_ alpha:CGFloat=1) {
  c.setStrokeColor(col(rgb,alpha));c.setLineWidth(width);c.move(to:CGPoint(x:x1,y:y1));c.addLine(to:CGPoint(x:x2,y:y2));c.strokePath()
 }
 func circle(_ x:CGFloat,_ y:CGFloat,_ r:CGFloat,_ rgb:[CGFloat],_ a:CGFloat=1) {
  c.setFillColor(col(rgb,a));c.fillEllipse(in:CGRect(x:x-r,y:y-r,width:r*2,height:r*2))
 }
 func piece(_ r:CGRect,_ name:String,_ seed:Int,_ amp:CGFloat=8,_ shadow:Bool=true) {
  let key="\(name)|\(seed)|\(r.width)|\(r.height)|\(amp)|\(shadow)";let pad:CGFloat=22
  let image:CGImage
  if let cached=pieceCache[key] {image=cached} else {
   let width=Int(ceil(r.width+pad*2)),height=Int(ceil(r.height+pad*2))
   let ctx=CGContext(data:nil,width:width,height:height,bitsPerComponent:8,bytesPerRow:0,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
   ctx.translateBy(x:pad,y:pad);let box=CGRect(x:0,y:0,width:r.width,height:r.height),path=torn(box,seed,amp)
   if shadow {ctx.saveGState();ctx.setShadow(offset:CGSize(width:4,height:7),blur:9,color:col(ink,0.20));ctx.addPath(path);ctx.setFillColor(col(paper));ctx.fillPath();ctx.restoreGState()}
   ctx.saveGState();ctx.addPath(path);ctx.clip();ctx.draw(textures[name]!,in:box);ctx.restoreGState()
   ctx.addPath(path);ctx.setStrokeColor(col([1,0.995,0.96],name=="dark" ? 0.10:0.50));ctx.setLineWidth(1);ctx.strokePath()
   image=ctx.makeImage()!;pieceCache[key]=image
  }
  c.draw(image,in:CGRect(x:r.minX-pad,y:r.minY-pad,width:CGFloat(image.width),height:CGFloat(image.height)))

 }
 func tape(_ x:CGFloat,_ y:CGFloat,_ angle:CGFloat) {
  c.saveGState();c.translateBy(x:x,y:y);c.rotate(by:angle)
  c.setAlpha(0.55);piece(CGRect(x:-73,y:-15,width:146,height:30),"yellow",90,4,false)
  for j in 0..<18 {line(-70+CGFloat(j)*8,-13,-70+CGFloat(j)*8,13,[0.85,0.73,0.39],0.4,0.3)}
  c.restoreGState()
 }
 // Large rough background scraps establish depth immediately.
 c.saveGState();c.translateBy(x:1460,y:60);c.rotate(by:0.11);piece(CGRect(x:0,y:0,width:620,height:1100),"dark",31,13);c.restoreGState()
 c.saveGState();c.translateBy(x:-30,y:900);c.rotate(by:-0.15);piece(CGRect(x:0,y:0,width:560,height:260),"yellow",53,14);c.restoreGState()
 // A halftone basketball is a printed collage scrap, not an additional chart.
 c.saveGState();c.translateBy(x:1850,y:1020);c.rotate(by:-0.3)
 for x in stride(from:CGFloat(-150),through:150,by:10) {for y in stride(from:CGFloat(-150),through:150,by:10) where x*x+y*y<150*150 {circle(x,y,2.5,paper,0.35)}}
 c.setStrokeColor(col(paper,0.65));c.setLineWidth(3)
 c.strokeEllipse(in:CGRect(x:-152,y:-152,width:304,height:304));c.strokeEllipse(in:CGRect(x:-60,y:-152,width:120,height:304));line(-152,0,152,0,paper,3,0.6)
 c.restoreGState()
 // Two title strips land independently; the words are part of the argument.
 let first=CGFloat(smooth((beat-0.05)/0.5)),second=CGFloat(smooth((beat-0.4)/0.65))
 c.saveGState();c.translateBy(x:-1100*(1-first),y:0);c.rotate(by:-0.012)
 piece(CGRect(x:93,y:46,width:605,height:91),"dark",2,7)
 text(titleLines[0],120,55,57,paper,true)
 c.restoreGState()
 c.saveGState();c.translateBy(x:-1280*(1-second),y:0);c.rotate(by:0.009)
 piece(CGRect(x:95,y:151,width:1100,height:130),"yellow",8,10)
 text(titleLines[1],124,156,88,titleInk,true)
 c.restoreGState()
 // Main torn page slides into position without changing the original chart type.
 let sheet=CGFloat(smooth((beat-1.05)/0.75))
 c.saveGState();c.translateBy(x:0,y:820*(1-sheet))
 piece(CGRect(x:70,y:308,width:1770,height:674),"paper",12,17)
 tape(164,311,-0.13);tape(1737,316,0.16)
 let left:CGFloat=216,right:CGFloat=1696,top:CGFloat=435,bottom:CGFloat=825
 let step=(right-left)/CGFloat(names.count),xs=(0..<names.count).map{left+step*(CGFloat($0)+0.5)}
 // Legend and axis names distinguish both original units explicitly.
 c.setFillColor(col(ink));c.fill(CGRect(x:150,y:348,width:20,height:20))
 text("每回合得分",184,340,28,ink,true)
 line(495,358,548,358,coral,5);circle(520,358,5,coral)
 text("有效命中率",561,340,28,coral,true)
 text("分 / 回合",144,382,21,muted)
 text("有效命中率",1765,382,21,coral,false,2)
 let axis=CGFloat(smooth((T-1.6)/0.5))
 for j in 0...6 {
  let y=bottom-CGFloat(j)/6*(bottom-top)
  line(left,y,right,y,j==0 ? ink:grid,j==0 ? 2:1.25,axis)
  text(j==0 ? "0":String(format:"%.1f",Double(j)*0.2),left-23,y-14,23,muted,false,2,axis)
  text("\(j*10)%",right+24,y-14,23,coral,false,0,axis)
 }
 let focus=showEmphasis ? CGFloat(smooth((T-6.2)/0.7)):0
 c.setFillColor(col(yellow,0.14*focus));c.fill(CGRect(x:xs[focusIndex]-79,y:top-15,width:158,height:bottom-top+85))
 for i in 0..<names.count {
  let cuts:[CGFloat]=[0,0.12,0.32,0.58,0.82,1];let cutIndex=max(0,min(5,Int(floor((T-2.0-Double(i)*0.18)*10))));let grow=cuts[cutIndex],height=CGFloat(ppp[i]/1.2)*(bottom-top)*grow
  let r=CGRect(x:xs[i]-55,y:bottom-height,width:110,height:height)
  if height>1 {
   c.saveGState();c.addPath(torn(r,i+50,1.5));c.clip();c.draw(textures[i==focusIndex && showEmphasis ? "yellow":"dark"]!,in:r);c.restoreGState()
  }
  let a=CGFloat(smooth((T-2.55-Double(i)*0.21)/0.3))
  text(String(format:"%.2f",ppp[i]),xs[i],bottom-height-51,34,ink,true,1,a,true)
  // Player labels are pasted on small rough paper tabs.
  piece(CGRect(x:xs[i]-88,y:847,width:176,height:49),"paper",120+i,3,false)
  text(names[i],xs[i],851,28,ink,true,1,axis)
 }
 let points=(0..<names.count).map{CGPoint(x:xs[$0],y:bottom-CGFloat(efg[$0]/60)*(bottom-top))}
 let progress=clamp((floor((T-4.05)*12)/12)/1.75)*Double(names.count-1)
 if T>=4.05 {
  let path=CGMutablePath();path.move(to:points[0])
  for i in 1..<names.count {let f=CGFloat(clamp(progress-Double(i-1)));if f>0 {path.addLine(to:CGPoint(x:points[i-1].x+(points[i].x-points[i-1].x)*f,y:points[i-1].y+(points[i].y-points[i-1].y)*f))}}
  c.setLineCap(.round);c.setLineJoin(.round)
  c.addPath(path);c.setStrokeColor(col(paper));c.setLineWidth(10);c.strokePath()
  c.addPath(path);c.setStrokeColor(col(coral));c.setLineWidth(5);c.strokePath()
  for i in 0..<names.count {let a=CGFloat(smooth((T-(4.05+Double(i)*1.75/Double(max(1,names.count-1))))/0.2));circle(points[i].x,points[i].y,8,paper,a);circle(points[i].x,points[i].y,5,coral,a)}
 }
 // Marker circle is drawn by hand around the original highest bar value.
 let mark=showEmphasis ? CGFloat(smooth((floor((T-6.65)*12)/12)/0.65)):0,cx=xs[focusIndex],cy=bottom-CGFloat(ppp[focusIndex]/1.2)*(bottom-top)-31
 if mark>0 {
  c.setStrokeColor(col(coral));c.setLineWidth(3.3);let path=CGMutablePath()
  for j in 0...Int(75*mark) {
   let a=CGFloat(j)/75*2*CGFloat.pi-0.7,x=cx+(69+2*sin(a*5))*cos(a),y=cy+(28+1.3*cos(a*3))*sin(a)
   if j==0 {path.move(to:CGPoint(x:x,y:y))} else {path.addLine(to:CGPoint(x:x,y:y))}
  };c.addPath(path);c.strokePath()
 }


 c.restoreGState()
 // The key number lands as its own clipped headline after the data reveal.
 let key=CGFloat(smooth((beat-6.35)/0.5))
 if key>0 && showEmphasis {
  c.saveGState();c.translateBy(x:1480,y:63-290*(1-key));c.rotate(by:-0.025)
  piece(CGRect(x:-30,y:0,width:349,height:216),"paper",69,10)
  piece(CGRect(x:-7,y:12,width:301,height:43),"yellow",70,5,false)
  text("这组球员中最高",142,13,24,ink,true,1)
  text(String(format:"%.2f",ppp[focusIndex]),141,48,113,ink,true,1,1,true)
  text(names[focusIndex]+" · 分 / 回合",142,166,25,ink,true,1)
  tape(160,0,0.02);c.restoreGState()
 }
}

let w=outputWidth,h=outputHeight,count=Int(duration*Double(outputFPS)),url=URL(fileURLWithPath:outputPath)
guard !FileManager.default.fileExists(atPath:outputPath) else {fatalError("Output already exists")}
let writer=try AVAssetWriter(outputURL:url,fileType:.mp4)
let input=AVAssetWriterInput(mediaType:.video,outputSettings:[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:w,AVVideoHeightKey:h,AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:12_000_000,AVVideoProfileLevelKey:AVVideoProfileLevelH264HighAutoLevel]])
let ad=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:input,sourcePixelBufferAttributes:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32BGRA,kCVPixelBufferWidthKey as String:w,kCVPixelBufferHeightKey as String:h,kCVPixelBufferCGImageCompatibilityKey as String:true,kCVPixelBufferCGBitmapContextCompatibilityKey as String:true])
writer.add(input);writer.shouldOptimizeForNetworkUse=true
guard writer.startWriting() else {fatalError("Cannot encode: \(String(describing:writer.error))")};writer.startSession(atSourceTime:.zero)
for frame in 0..<count {
 while !input.isReadyForMoreMediaData {Thread.sleep(forTimeInterval:0.001)}
 autoreleasepool {
  var p:CVPixelBuffer?;CVPixelBufferPoolCreatePixelBuffer(nil,ad.pixelBufferPool!,&p);let pixel=p!
  CVPixelBufferLockBaseAddress(pixel,[])
  let c=CGContext(data:CVPixelBufferGetBaseAddress(pixel),width:w,height:h,bitsPerComponent:8,bytesPerRow:CVPixelBufferGetBytesPerRow(pixel),space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.noneSkipFirst.rawValue|CGBitmapInfo.byteOrder32Little.rawValue)!
  c.translateBy(x:0,y:CGFloat(h));c.scaleBy(x:CGFloat(w)/1920,y:-CGFloat(h)/1080)
  draw(c,Double(frame)/Double(outputFPS),false)
  CVPixelBufferUnlockBaseAddress(pixel,[])
  guard ad.append(pixel,withPresentationTime:CMTime(value:Int64(frame),timescale:outputFPS)) else {fatalError("Cannot append")}
 }
}
input.markAsFinished();let sem=DispatchSemaphore(value:0);writer.finishWriting{sem.signal()};sem.wait()
guard writer.status == .completed else {fatalError("Cannot finish")}
let gen=AVAssetImageGenerator(asset:AVURLAsset(url:url));for frame in [0,count/2,count-1] {_ = try gen.copyCGImage(at:CMTime(value:Int64(frame),timescale:outputFPS),actualTime:nil)}
print("Verified \(w)x\(h), \(duration)s, \(outputFPS)fps; render+encode \(Date().timeIntervalSince(renderStart)) seconds")
