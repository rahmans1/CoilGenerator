import csv
import sys
import os
import math

output_file="upstream"
cm=10


s_x=4.866*cm
s_y=1.01*cm
s_l_arm=math.sqrt(math.pow((25.210-24.751),2)+math.pow((789.132-610.832),2))*cm
s_rad=(6.044+4.866)*cm    
s_theta= math.atan((25.210-24.751)/(789.132-610.832))
len_ucoil=2*s_rad+s_l_arm
z_origin=s_rad-len_ucoil/2


pos=2.928*cm+math.sqrt(math.pow(s_rad,2)+math.pow(s_l_arm/2,2))*math.sin(math.atan(2*s_rad/s_l_arm)+s_theta)
#theta=math.atan(()/)

f=open(output_file+".gdml", "w+")


f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<gdml\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n")
f.write("\n\n<define>\n</define>")


f.write("\n\n<solids>\n")
f.write("\t<box name=\"solid_s_arm_low\" lunit=\"mm\" x=\""+str(s_x)+"\" y=\""+str(s_y)+"\" z=\""+str(s_l_arm)+"\"/>\n")
f.write("\t<box name=\"solid_s_arm_up\" lunit=\"mm\" x=\""+str(s_x)+"\" y=\""+str(s_y)+"\" z=\""+str(s_l_arm)+"\"/>\n")
f.write("\t<tube name=\"solid_s_frontNose\" rmin=\""+str(s_rad-s_x)+"\"  rmax=\""+str(s_rad)+"\" z=\""+str(s_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n")
f.write("\t<tube name=\"solid_s_endNose\" rmin=\""+str(s_rad-s_x)+"\"  rmax=\""+str(s_rad)+"\" z=\""+str(s_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n")
f.write("\t<box name=\"solid_ucoil\" lunit=\"mm\" x=\""+str(2*s_rad)+"\" y=\""+str(s_y)+"\" z=\""+str(len_ucoil)+"\"/>\n")


f.write("\t<union name=\"solid_s_1\">\n\t\t<first ref=\"solid_s_frontNose\"/>\n\t\t<second ref=\"solid_s_arm_up\"/>\n\t\t<position name=\"pos_s_1\" x=\""+str(s_rad-s_x/2)+"\" y=\""+str(-s_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")
f.write("\t<union name=\"solid_s_2\">\n\t\t<first ref=\"solid_s_1\"/>\n\t\t<second ref=\"solid_s_arm_low\"/>\n\t\t<position name=\"pos_s_2\" x=\""+str(-s_rad+s_x/2)+"\" y=\""+str(-s_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s_2\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")
f.write("\t<union name=\"solid_s\">\n\t\t<first ref=\"solid_s_2\"/>\n\t\t<second ref=\"solid_s_endNose\"/>\n\t\t<position name=\"pos_s_3\" x=\""+str(0)+"\" y=\""+str(-s_l_arm)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s_3\" x=\"-pi\" y=\"0\" z=\"0\"/>\n\t</union>\n")



f.write("\t<cone name=\"solid_upstreamToroidMother\" rmin1=\""+str(29.28-0.5)+"\"  rmax1=\""+str(252.10+0.5)+"\" rmin2=\""+str(33.87-0.5)+"\" rmax2=\""+str(252.10+0.5)+"\"  z=\""+str(s_l_arm+2*s_rad+1)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n") #Make sure this mother volume doesn't interfere with coils
f.write("</solids>\n")



f.write("\n\n<structure>\n")

for i in range(0,1):
	f.write("\t<volume name=\"logic_s_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_s\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")

	f.write("\t<volume name=\"logic_ucoil_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_ucoil\"/>\n")
	f.write("\t\t<physvol name=\"s_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_s_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_s_"+str(i)+"\" x=\""+str(0)+"\" y=\"0\" z=\""+str(z_origin)+"\"/>\n\t\t\t<rotation name=\"rot_s_"+str(i)+"\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t</volume>\n")


f.write("\t<volume name=\"upstreamToroidMother\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_upstreamToroidMother\"/>\n")

for i in range(0,1):
        rpos=pos
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
	f.write("\t\t<physvol name=\"ucoil_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_ucoil_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_ucoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\"0\"/>\n\t\t\t<rotation name=\"rot_ucoil_"+str(i)+"\" x=\"0\" y=\""+str(-s_theta)+"\" z=\""+str(-theta)+"\"/>\n\t\t</physvol>\n")
f.write("\t</volume>\n")

f.write("</structure>\n")

f.write("<setup name=\"upstreamToroidWorld\" version=\"1.0\">\n\t<world ref=\"upstreamToroidMother\"/>\n</setup>\n")

f.write("</gdml>")




"""
    <physvol name="s_arm_low">
      <volumeref ref="logic_s_arm_low"/>
      <position name="pos_s_arm_low" x="-60-10" y="0" z="0"/>
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
  <volume name="logic_s_arm_low">
    <materialref ref="G4_Cu"/>
    <solidref ref="solid_s_arm_low"/>
    <auxiliary auxtype="Color" auxvalue="red"/>
  </volume>

  <volume name="logic_frontNose">
    <materialref ref="G4_Cu"/>
    <solidref ref="solid_s_frontNose"/>
    <auxiliary auxtype="Color" auxvalue="blue"/>
  </volume>

  <volume name="logic_endNose">
    <materialref ref="G4_Cu"/>
    <solidref ref="solid_s_frontNose"/>
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








