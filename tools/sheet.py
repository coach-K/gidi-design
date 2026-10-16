import sys; from PIL import Image
out=sys.argv[1]; fs=sys.argv[2:]; W=960
ims=[Image.open(f) for f in fs]; ims=[i.resize((W,int(W*i.height/i.width))) for i in ims]
H=sum(i.height for i in ims[::2])+10*len(ims); s=Image.new('RGB',(2*W+10,H),'white'); y=0
for k in range(0,len(ims),2):
    s.paste(ims[k],(0,y)); 
    if k+1<len(ims): s.paste(ims[k+1],(W+10,y))
    y+=ims[k].height+10
s.save(out)
