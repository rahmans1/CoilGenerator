import csv
import sys
import os
import math

output_file="upstreamToroid"
cm=10

s_x=4.866*cm
s_y=1.01*cm
s_l_arm=math.sqrt(math.pow((25.210-24.751),2)+math.pow((789.132-610.832),2))*cm
s_rad=(6.044+4.866)*cm    
s_theta= math.atan((25.210-24.751)/(789.132-610.832))
len_ucoil=2*s_rad+s_l_arm
z_origin=s_rad-len_ucoil/2

len_mother=len_ucoil+20

pos=2.928*cm+math.sqrt(math.pow(s_rad,2)+math.pow(s_l_arm/2,2))*math.sin(math.atan(2*s_rad/s_l_arm)+s_theta)


f=open(output_file+".gdml", "w+")

out="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
out+="<gdml"
out+="\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
out+="\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n"
out+="\n\n<define>"
out+="\n</define>"


out+="\n\n<solids>\n"
out+="\t<box name=\"solid_s_arm_low\" lunit=\"mm\" x=\""+str(s_x)+"\" y=\""+str(s_y)+"\" z=\""+str(s_l_arm)+"\"/>\n"
out+="\t<box name=\"solid_s_arm_up\" lunit=\"mm\" x=\""+str(s_x)+"\" y=\""+str(s_y)+"\" z=\""+str(s_l_arm)+"\"/>\n"
out+="\t<tube name=\"solid_s_frontNose\" rmin=\""+str(s_rad-s_x)+"\"  rmax=\""+str(s_rad)+"\" z=\""+str(s_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
out+="\t<tube name=\"solid_s_endNose\" rmin=\""+str(s_rad-s_x)+"\"  rmax=\""+str(s_rad)+"\" z=\""+str(s_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
out+="\t<box name=\"solid_ucoil\" lunit=\"mm\" x=\""+str(2*s_rad)+"\" y=\""+str(len_ucoil)+"\" z=\""+str(s_y)+"\"/>\n"

out+="\t<union name=\"solid_s_1\">"
out+="\n\t\t<first ref=\"solid_s_frontNose\"/>"
out+="\n\t\t<second ref=\"solid_s_arm_up\"/>"
out+="\n\t\t<position name=\"pos_s_1\" x=\""+str(s_rad-s_x/2)+"\" y=\""+str(-s_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"
out+="\t<union name=\"solid_s_2\">"
out+="\n\t\t<first ref=\"solid_s_1\"/>"
out+="\n\t\t<second ref=\"solid_s_arm_low\"/>"
out+="\n\t\t<position name=\"pos_s_2\" x=\""+str(-s_rad+s_x/2)+"\" y=\""+str(-s_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s_2\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"
out+="\t<union name=\"solid_s\">"
out+="\n\t\t<first ref=\"solid_s_2\"/>"
out+="\n\t\t<second ref=\"solid_s_endNose\"/>"
out+="\n\t\t<position name=\"pos_s_3\" x=\""+str(0)+"\" y=\""+str(-s_l_arm)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s_3\" x=\"-pi\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\t<cone name=\"solid_upstreamToroidMother\" rmin1=\""+str(29.28-0.5)+"\"  rmax1=\""+str(252.10+0.5)+"\" rmin2=\""+str(33.87-0.5)+"\" rmax2=\""+str(252.10+0.5)+"\"  z=\""+str(len_mother)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n" #Make sure this mother volume doesn't interfere with coils
out+="</solids>\n"

out+="\n\n<structure>\n"

for i in range(0,7):
        out+="\t<volume name=\"logic_s_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cu\"/>"
        out+="\n\t\t<solidref ref=\"solid_s\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"magenta\"/>"
        out+="\n\t\t<auxiliary auxtype=\"SensDet\" auxvalue=\"coilDet\"/>"
        out+="\n\t\t<auxiliary auxtype=\"DetNo\" auxvalue=\""+str(4000+i+1)+"\"/>"
        out+="\n\t</volume>\n"
        
            
        out+="\t<volume name=\"logic_ucoil_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
        out+="\n\t\t<solidref ref=\"solid_ucoil\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"
        out+="\n\t\t<physvol name=\"s_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_s_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_logic_s_"+str(i)+"\" x=\""+str(0)+"\" y=\""+str(-z_origin)+"\" z=\""+str(0)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_logic_s_"+str(i)+"\" x=\"0\" y=\"0\" z=\"0\"/>"        
        out+="\n\t\t</physvol>"
        out+="\n\t</volume>\n"
        

out+="\t<volume name=\"upstreamToroidMother\">"
out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
out+="\n\t\t<solidref ref=\"solid_upstreamToroidMother\"/>"
out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"

for i in range(0,7):
        rpos=pos
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
	out+="\n\t\t<physvol name=\"ucoil_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_ucoil_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_ucoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\""+str(0)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_ucoil_"+str(i)+"\" x=\"pi/2\" y=\""+str(theta)+"\" z=\""+str(-s_theta)+"\"/>"
        out+="\n\t\t</physvol>"

out+="\n\t</volume>"


out+="\n</structure>\n"

out+="<setup name=\"upstreamToroidWorld\" version=\"1.0\">"
out+="\n\t<world ref=\"upstreamToroidMother\"/>"
out+="\n</setup>\n"

out+="</gdml>"

f.write(out)



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
	out+="<xtru name=\"solidLintel"+str(i+1)+"\" lunit=\"mm\">\n"
        out+=" <twoDimVertex x=\""+str(extent)+"\" y=\""+str(b_outer_new)+"\" />\n"
 	out+=" <twoDimVertex x=\""+str(extent)+"\" y=\""+str(-b_outer_new)+"\" />\n"
        out+=" <twoDimVertex x=\""+str(-extent)+"\" y=\""+str(-b_inner_new)+"\" />\n"
        out+=" <twoDimVertex x=\""+str(-extent)+"\" y=\""+str(b_inner_new)+"\" />\n"
        out+=" <section zOrder=\"1\" zPosition=\""+str(-thickness/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\" />\n"
        out+=" <section zOrder=\"2\" zPosition=\""+str(thickness/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\" />\n"
        out+="</xtru>\n\n");

for i in range(0,7):
	out+="<volume name=\"logicLintel"+str(i+1)+"\">
        out+="\n<materialref ref=\"Lead\"/>"
        out+="\n<solidref ref=\"solidLintel"+str(i+1)+"\"/>"
        out+="\n</volume>\n\n"



for i in range(0,1):
        th=i*2*math.pi/7+math.pi
        x= r_center*math.cos(th)
        y= r_center*math.sin(th)
        z= 12800+thickness/2
	out+="<physvol name=\"lintel"+str(i+1)+"\">\n"
        out+=" <volumeref ref=\"logicLintel"+str(i+1)+"\"/>\n"
        out+=" <position name=\"lintel"+str(i+1)+"pos\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(z)+"-DOFFSET\"/>\n"
        out+=" <rotation name=\"lintel"+str(i+1)+"rot\" x=\"0\" y=\"0\" z=\""+str(-th)+"\"/>\n"
        out+="</physvol>\n"
"""











