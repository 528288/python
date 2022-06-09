from PIL import Image
import os
import os.path
 
rootdir = r'./image/'  # 原图
 
for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        currentPath = os.path.join(parent, filename)
        im = Image.open(currentPath)  # 打开图片
        def iter_frames(im):
            try:
                i= 0
                while 1:
                    im.seek(i)
                    imframe = im.copy()
                    if i == 0:
                        palette = imframe.getpalette()
                    else:
                        imframe.putpalette(palette)
                    yield imframe
                    i += 1
            except EOFError:
                pass   
        for i, frame in enumerate(iter_frames(im)):
            frame.save(r"./img_out"+'\\'+filename +'.gif',**frame.info)   # 如果要转其他格式，修改.gif就可以了
