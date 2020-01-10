import csv
import sys
import os
import math

output_file="downstream"
cm=10

x_origin=0
z_origin=0



s1_x=2*cm         # extent along x
s1_y=1*cm         # extent along y
s1_length_straight=(1100-1000)*cm  # length of segment
s1_radius=(14-6)/2*cm     # minimum radius at front end   
s1_xpos=(12-x_origin)*cm
s1_zpos=(1050-z_origin)*cm
s1_theta=0.02     # slant angle of upper arm of segment 1





f=open(output_file+".gdml", "w+")


f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<gdml\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n")
f.write("\n\n<define>\n</define>")


f.write("\n\n<solids>\n")
f.write("\t<box name=\"solid_lowerStraightSegment\" lunit=\"mm\" x=\""+str(s1_x)+"\" y=\""+str(y)+"\" z=\""+str(length_straight)+"\"/>\n")
f.write("\t<para name=\"solid_upperStraightSegment\" lunit=\"mm\" aunit=\"rad\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(length_straight)+"\" alpha=\"0\" theta=\""+str(s1_theta)+"\" phi=\"0\"/>\n")
f.write("\t<tube name=\"solid_frontNose\" rmin=\""+str(radius)+"\"  rmax=\""+str(radius+x)+"\" z=\""+str(y)+"\" startphi=\"0\" deltaphi=\"180\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("\t<tube name=\"solid_endNose\" rmin=\""+str(radius)+"\"  rmax=\""+str(radius+x)+"\" z=\""+str(y)+"\" startphi=\"0\" deltaphi=\"180\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("\t<box name=\"solid_ucoil\" lunit=\"mm\" x=\""+str(360)+"\" y=\""+str(60)+"\" z=\""+str(8000)+"\"/>\n")


f.write("\t<tube name=\"solid_downstreamToroidMother\" rmin=\""+str(pos-x-radius-1)+"\"  rmax=\""+str(pos+x+radius+1)+"\" z=\""+str(length_straight+2*radius+2*x+1)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("</solids>\n")



f.write("\n\n<structure>\n")

for i in range(0,1):
	f.write("\t<volume name=\"logic_upperStraightSegment_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_upperStraightSegment\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
	f.write("\t<volume name=\"logic_lowerStraightSegment_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_lowerStraightSegment\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
	f.write("\t<volume name=\"logic_frontNose_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_frontNose\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
#	f.write("\t<volume name=\"logic_endNose_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_endNose\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")


	f.write("\t<volume name=\"logic_ucoil_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_ucoil\"/>\n")
	f.write("\t\t<physvol name=\"upperStraightSegment_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_upperStraightSegment_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_upperStraightSegment_"+str(i)+"\" x=\""+str(radius+x/2+length_straight/2*math.tan(s1_theta))+"\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t\t<physvol name=\"lowerStraightSegment_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_lowerStraightSegment_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_lowerStraightSegment_"+str(i)+"\" x=\""+str(-radius-x/2)+"\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t\t<physvol name=\"frontNose_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_frontNose_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_frontNose_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-length_straight/2)+"\"/>\n\t\t\t<rotation name=\"rot_frontNose_"+str(i)+"\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
#	f.write("\t\t<physvol name=\"endNose_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_endNose_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_endNose_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(length_straight/2)+"\"/>\n\t\t\t<rotation name=\"rot_endNose_"+str(i)+"\" x=\"-pi/2\" y=\"0\" z=\"0\"/>\n\t\t</physvol>\n")
	f.write("\t</volume>\n")


f.write("\t<volume name=\"downstreamToroidMother\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_downstreamToroidMother\"/>\n")

for i in range(0,1):
        rpos=pos
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
	f.write("\t\t<physvol name=\"ucoil_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_ucoil_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_ucoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\"0\"/>\n\t\t\t<rotation name=\"rot_ucoil_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-theta)+"\"/>\n\t\t</physvol>\n")
f.write("\t</volume>\n")

f.write("</structure>\n")

f.write("<setup name=\"downstreamToroidWorld\" version=\"1.0\">\n\t<world ref=\"downstreamToroidMother\"/>\n</setup>\n")

f.write("</gdml>")












