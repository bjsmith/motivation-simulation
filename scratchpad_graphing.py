import pylab as p 

f0 = p.figure() 
f1 = p.figure() 
ax0 = f0.add_subplot(111) 
ax0.plot(range(0,50))
ax1 = f1.add_subplot(111) 
ax1.plot(range(0,20))
p.pause(2)

ax1.text(0,1,"This is updatable",weight='bold',fontsize=16)
p.figure(f1.number)

ax0.text(0,1,"This one, drawn first, is not.",weight='bold',fontsize=16)
p.figure(f0.number)
#
p.pause(10)
#p.show()
