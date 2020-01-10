import csv
import sys
import os
import math

output_file="upstream"
cm=10


x=4.87*cm
y=1.01*cm
length_straight=(789.14-610.84)*cm
radius=(19.88-7.79)/2*cm    
pos=7.79*cm+radius

f=open(output_file+".gdml", "w+")


f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<gdml\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n")
f.write("\n\n<define>\n</define>")


f.write("\n\n<solids>\n")
f.write("\t<box name=\"solid_lowerStraightSegment\" lunit=\"mm\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(length_straight)+"\"/>\n")
f.write("\t<box name=\"solid_upperStraightSegment\" lunit=\"mm\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(length_straight)+"\"/>\n")
f.write("\t<tube name=\"solid_frontNose\" rmin=\""+str(radius)+"\"  rmax=\""+str(radius+x)+"\" z=\""+str(y)+"\" startphi=\"0\" deltaphi=\"180\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("\t<tube name=\"solid_endNose\" rmin=\""+str(radius)+"\"  rmax=\""+str(radius+x)+"\" z=\""+str(y)+"\" startphi=\"0\" deltaphi=\"180\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("\t<box name=\"solid_ucoil\" lunit=\"mm\" x=\""+str(2*x+2*radius)+"\" y=\""+str(y)+"\" z=\""+str(length_straight+2*radius+2*x)+"\"/>\n")


f.write("\t<tube name=\"solid_upstreamToroidMother\" rmin=\""+str(pos-x-radius-1)+"\"  rmax=\""+str(pos+x+radius+1)+"\" z=\""+str(length_straight+2*radius+2*x+1)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("</solids>\n")



f.write("\n\n<structure>\n")

for i in range(0,7):
	f.write("\t<volume name=\"logic_upperStraightSegment_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_upperStraightSegment\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
	f.write("\t<volume name=\"logic_lowerStraightSegment_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_lowerStraightSegment\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
	f.write("\t<volume name=\"logic_frontNose_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_frontNose\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
	f.write("\t<volume name=\"logic_endNose_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_endNose\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")


	f.write("\t<volume name=\"logic_ucoil_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_ucoil\"/>\n")
	f.write("\t\t<physvol name=\"upperStraightSegment_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_upperStraightSegment_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_upperStraightSegment_"+str(i)+"\" x=\""+str(radius+x/2)+"\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t\t<physvol name=\"lowerStraightSegment_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_lowerStraightSegment_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_lowerStraightSegment_"+str(i)+"\" x=\""+str(-radius-x/2)+"\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t\t<physvol name=\"frontNose_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_frontNose_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_frontNose_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-length_straight/2)+"\"/>\n\t\t\t<rotation name=\"rot_frontNose_"+str(i)+"\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t\t<physvol name=\"endNose_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_endNose_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_endNose_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(length_straight/2)+"\"/>\n\t\t\t<rotation name=\"rot_endNose_"+str(i)+"\" x=\"-pi/2\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t</volume>\n")


f.write("\t<volume name=\"upstreamToroidMother\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_upstreamToroidMother\"/>\n")

for i in range(0,7):
        rpos=pos
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
	f.write("\t\t<physvol name=\"ucoil_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_ucoil_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_ucoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\"0\"/>\n\t\t\t<rotation name=\"rot_ucoil_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-theta)+"\"/>\n\t\t</physvol>\n")
f.write("\t</volume>\n")

f.write("</structure>\n")

f.write("<setup name=\"upstreamToroidWorld\" version=\"1.0\">\n\t<world ref=\"upstreamToroidMother\"/>\n</setup>\n")

f.write("</gdml>")




"""
    <physvol name="lowerStraightSegment">
      <volumeref ref="logic_lowerStraightSegment"/>
      <position name="pos_lowerStraightSegment" x="-60-10" y="0" z="0"/>
    </physvol>

    <physvol name="frontNose">
      <volumeref ref="logic_frontNose"/>
      <position name="pos_frontNose" x="0" y="0" z="-120/2"/>
      <rotation name="rot_frontNose" x="pi/2" y="0" z="0"/>
    </physvol>

    <physvol name="endNose">
      <volumeref ref="logic_endNose"/>
      <position name="pos_frontNose" x="0" y="0" z="120/2"/>
      <rotation name="rot_frontNose" x="-pi/2" y="0" z="0"/>
    </physvol>

  </volume>
"""

"""
  <volume name="logic_lowerStraightSegment">
    <materialref ref="G4_Cu"/>
    <solidref ref="solid_lowerStraightSegment"/>
    <auxiliary auxtype="Color" auxvalue="red"/>
  </volume>

  <volume name="logic_frontNose">
    <materialref ref="G4_Cu"/>
    <solidref ref="solid_frontNose"/>
    <auxiliary auxtype="Color" auxvalue="blue"/>
  </volume>

  <volume name="logic_endNose">
    <materialref ref="G4_Cu"/>
    <solidref ref="solid_frontNose"/>
    <auxiliary auxtype="Color" auxvalue="blue"/>
  </volume>
"""














"""

for i in range(0,1):
	f.write("<xtru name=\"solidLintel"+str(i+1)+"\" lunit=\"mm\">\n")
        f.write(" <twoDimVertex x=\""+str(extent)+"\" y=\""+str(b_outer_new)+"\" />\n")
 	f.write(" <twoDimVertex x=\""+str(extent)+"\" y=\""+str(-b_outer_new)+"\" />\n")
        f.write(" <twoDimVertex x=\""+str(-extent)+"\" y=\""+str(-b_inner_new)+"\" />\n")
        f.write(" <twoDimVertex x=\""+str(-extent)+"\" y=\""+str(b_inner_new)+"\" />\n")
        f.write(" <section zOrder=\"1\" zPosition=\""+str(-thickness/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\" />\n")
        f.write(" <section zOrder=\"2\" zPosition=\""+str(thickness/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\" />\n")
        f.write("</xtru>\n\n");

for i in range(0,7):
	f.write("<volume name=\"logicLintel"+str(i+1)+"\">\n<materialref ref=\"Lead\"/>\n<solidref ref=\"solidLintel"+str(i+1)+"\"/>\n</volume>\n\n")



for i in range(0,1):
        th=i*2*math.pi/7+math.pi
        x= r_center*math.cos(th)
        y= r_center*math.sin(th)
        z= 12800+thickness/2
	f.write("<physvol name=\"lintel"+str(i+1)+"\">\n")
        f.write(" <volumeref ref=\"logicLintel"+str(i+1)+"\"/>\n")
        f.write(" <position name=\"lintel"+str(i+1)+"pos\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(z)+"-DOFFSET\"/>\n")
        f.write(" <rotation name=\"lintel"+str(i+1)+"rot\" x=\"0\" y=\"0\" z=\""+str(-th)+"\"/>\n")
        f.write("</physvol>\n")
"""








