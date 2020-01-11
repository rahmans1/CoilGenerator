import csv
import sys
import os
import math

output_file="downstream"
cm=10

# global coordinate of coil center
x_origin=0
z_origin=0

# segment 1
s1_x=2*cm         # extent along x
s1_y=1*cm         # extent along y
s1_l_arm=(1100-1000)*cm  # length of arms
s1_rad=(16-4)/2*cm     # arc rad of nose  
s1_xpos=(12-x_origin)*cm # center of straight part
s1_zpos=(1050-z_origin)*cm # center of straight part
s1_theta=math.atan((16.0-14)*cm/s1_l_arm)     # slant angle of upper arm

# segment 2
s2_x=1*cm 
s2_y=1*cm 
s2_l_arm=(1200-1100)*cm # length of arms
s2_rad=(s1_rad-s1_x+s1_l_arm/2*math.tan(s1_theta)) # arc rad of nose
s2_xpos=0*cm # center of straight part
s2_zpos=0*cm # center of straight part
s2_theta=math.atan((23.0-17)*cm/s2_l_arm)

# segment 3
s3_x=2*cm
s3_y=1*cm
s3_l_arm=(1300-1200)*cm
s3_rad=(s2_rad-s2_x+s2_l_arm/2*math.tan(s2_theta))
s3_xpos=0*cm
s3_zpos=0*cm
s3_theta=math.atan((26.0-23)*cm/s3_l_arm)


f=open(output_file+".gdml", "w+")


f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<gdml\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n")
f.write("\n\n<define>\n</define>")


f.write("\n\n<solids>\n")
f.write("\t<box name=\"solid_s1_lowerArm\" lunit=\"mm\" x=\""+str(s1_x)+"\" y=\""+str(s1_y)+"\" z=\""+str(s1_l_arm)+"\"/>\n")
f.write("\t<para name=\"solid_s1_upperArm\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s1_x)+"\" y=\""+str(s1_y)+"\" z=\""+str(s1_l_arm)+"\" alpha=\"0\" theta=\""+str(s1_theta)+"\" phi=\"0\"/>\n")
f.write("\t<tube name=\"solid_s1_frontNose\" rmin=\""+str(s1_rad-s1_x)+"\"  rmax=\""+str(s1_rad)+"\" z=\""+str(s1_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n")

f.write("\t<box name=\"solid_s2_lowerArm\" lunit=\"mm\" x=\""+str(s1_x+s2_x)+"\" y=\""+str(s2_y)+"\" z=\""+str(s2_l_arm)+"\"/>\n")
f.write("\t<para name=\"solid_s2_upperArm\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s1_x+s2_x)+"\" y=\""+str(s2_y)+"\" z=\""+str(s2_l_arm)+"\" alpha=\"0\" theta=\""+str(s2_theta)+"\" phi=\"0\"/>\n")
f.write("\t<tube name=\"solid_s2_frontNose\" rmin=\""+str(s2_rad-s2_x)+"\"  rmax=\""+str(s2_rad)+"\" z=\""+str(s2_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n")

f.write("\t<box name=\"solid_s3_lowerArm\" lunit=\"mm\" x=\""+str(s1_x+s2_x+s3_x)+"\" y=\""+str(s3_y)+"\" z=\""+str(s3_l_arm)+"\"/>\n")
f.write("\t<para name=\"solid_s3_upperArm\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s1_x+s2_x+s3_x)+"\" y=\""+str(s3_y)+"\" z=\""+str(s3_l_arm)+"\" alpha=\"0\" theta=\""+str(s3_theta)+"\" phi=\"0\"/>\n")
f.write("\t<tube name=\"solid_s3_frontNose\" rmin=\""+str(s3_rad-s3_x)+"\"  rmax=\""+str(s3_rad)+"\" z=\""+str(s3_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n")




f.write("\t<union name=\"solid_s1_1\">\n\t\t<first ref=\"solid_s1_frontNose\"/>\n\t\t<second ref=\"solid_s1_upperArm\"/>\n\t\t<position name=\"pos_s1_1\" x=\""+str(s1_rad-s1_x/2+s1_l_arm/2*math.tan(s1_theta))+"\" y=\""+str(-s1_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s1_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")
f.write("\t<union name=\"solid_s1\">\n\t\t<first ref=\"solid_s1_1\"/>\n\t\t<second ref=\"solid_s1_lowerArm\"/>\n\t\t<position name=\"pos_s1\" x=\""+str(-s1_rad+s1_x/2)+"\" y=\""+str(-s1_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s1\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")

f.write("\t<union name=\"solid_s2_1\">\n\t\t<first ref=\"solid_s2_frontNose\"/>\n\t\t<second ref=\"solid_s2_upperArm\"/>\n\t\t<position name=\"pos_s2_1\" x=\""+str(s2_rad-s2_x/2+s1_x/2+s2_l_arm/2*math.tan(s2_theta))+"\" y=\""+str(-s2_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s2_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")
f.write("\t<union name=\"solid_s2\">\n\t\t<first ref=\"solid_s2_1\"/>\n\t\t<second ref=\"solid_s2_lowerArm\"/>\n\t\t<position name=\"pos_s2\" x=\""+str(-s2_rad+s2_x/2-s1_x/2)+"\" y=\""+str(-s2_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s2\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")

f.write("\t<union name=\"solid_s3_1\">\n\t\t<first ref=\"solid_s3_frontNose\"/>\n\t\t<second ref=\"solid_s3_upperArm\"/>\n\t\t<position name=\"pos_s3_1\" x=\""+str(s3_rad-s3_x/2+(s1_x+s2_x)/2+s3_l_arm/2*math.tan(s3_theta))+"\" y=\""+str(-s3_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s3_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")
f.write("\t<union name=\"solid_s3\">\n\t\t<first ref=\"solid_s3_1\"/>\n\t\t<second ref=\"solid_s3_lowerArm\"/>\n\t\t<position name=\"pos_s3\" x=\""+str(-s3_rad+s3_x/2-(s1_x+s2_x)/2)+"\" y=\""+str(-s3_l_arm/2)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s3\" x=\"pi/2\" y=\"0\" z=\"0\"/>\n\t</union>\n")

f.write("\t<union name=\"solid_s1_s2\">\n\t\t<first ref=\"solid_s1\"/>\n\t\t<second ref=\"solid_s2\"/>\n\t\t<position name=\"pos_s1_s2\" x=\""+str(s1_l_arm/2*math.tan(s1_theta))+"\" y=\""+str(-s1_l_arm)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s2\" x=\"0\" y=\"0\" z=\"0\"/>\n\t</union>\n")
f.write("\t<union name=\"solid_s1_s2_s3\">\n\t\t<first ref=\"solid_s1_s2\"/>\n\t\t<second ref=\"solid_s3\"/>\n\t\t<position name=\"pos_s1_s2_s3\" x=\""+str(s1_l_arm/2*math.tan(s1_theta)+s2_l_arm/2*math.tan(s2_theta))+"\" y=\""+str(-s1_l_arm-s2_l_arm)+"\" z=\"0\"/>\n\t\t<rotation name=\"rot_s2\" x=\"0\" y=\"0\" z=\"0\"/>\n\t</union>\n")


f.write("\t<box name=\"solid_dcoil\" lunit=\"mm\" x=\""+str(360)+"\" y=\""+str(60)+"\" z=\""+str(2000)+"\"/>\n")
f.write("\t<tube name=\"solid_DS_toroidMother\" rmin=\""+str(0)+"\"  rmax=\""+str(1000)+"\" z=\""+str(8000)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n")
f.write("</solids>\n")



f.write("\n\n<structure>\n")

for i in range(0,1):
	f.write("\t<volume name=\"logic_s1_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Cu\"/>\n\t\t<solidref ref=\"solid_s1_s2_s3\"/>\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>\n\t</volume>\n")
        
	f.write("\t<volume name=\"logic_dcoil_"+str(i)+"\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_dcoil\"/>\n")
        f.write("\t\t<physvol name=\"s1_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_s1_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_s1_"+str(i)+"\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\"0\"/>\n\t\t\t<rotation name=\"rot_s1_"+str(i)+"\" x=\"pi/2\" y=\"0\" z=\""+str(0)+"\"/>\n\t\t</physvol>\n")
	f.write("\t</volume>\n")


f.write("\t<volume name=\"DS_toroidMother\">\n\t\t<materialref ref=\"G4_Galactic\"/>\n\t\t<solidref ref=\"solid_DS_toroidMother\"/>\n")

for i in range(0,1):
        rpos=0
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
	f.write("\t\t<physvol name=\"dcoil_"+str(i)+"\">\n\t\t\t<volumeref ref=\"logic_dcoil_"+str(i)+"\"/>\n\t\t\t<position name=\"pos_dcoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\"0\"/>\n\t\t\t<rotation name=\"rot_dcoil_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-theta)+"\"/>\n\t\t</physvol>\n")
f.write("\t</volume>\n")

f.write("</structure>\n")

f.write("<setup name=\"DS_toroidWorld\" version=\"1.0\">\n\t<world ref=\"DS_toroidMother\"/>\n</setup>\n")

f.write("</gdml>")












