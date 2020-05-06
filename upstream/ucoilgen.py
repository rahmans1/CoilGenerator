#!/usr/bin/env python
import csv
import sys
import os
import subprocess
import math
import time
import argparse



parser= argparse.ArgumentParser(description="Generate a segmented coil based on given parameters. Example: ./dcoilgen.py -l segmented.list -f test")
parser.add_argument("-l", dest="par_list", action="store", required=False, help="Provide the list of parameters. This is different for each of the coil types.")
parser.add_argument("-f", dest="output_file", action="store", required=False, default="DSToroid.gdml", help="Provide the required output file location")

args=parser.parse_args()
output_file=os.path.realpath(args.output_file)


p={}    # dictionary of parameter values

with open(args.par_list) as csvfile:
     reader=csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in reader:
         p[row[0]]=float(row[1])

 
p["C_l_arm"]= p["C_z2_up"]-p["C_z1_up"]
p["C_rad_front"]= (p["C_x1_up"]-p["C_x1_low"])/2.0
p["C_rad_back"]= (p["C_x2_up"]-p["C_x2_low"])/2.0
p["C_rpos"]=p["C_x1_low"]+ p["C_rad_front"]
p["C_zpos"]=p["C_z1_up"]+p["C_l_arm"]/2-7000   ## The 7000 needs to be the center of the mother volume


r_inner_mother=20
r_outer_mother=420
l_mother=8000

out=""

out+="\n\n<materials>\n"
out+="\t<material name=\"G4_CW95\" state=\"solid\">\n"
out+="\t\t<D value=\"18.0\" unit=\"g/cm3\"/>\n"
out+="\t\t<fraction n=\"0.9500\" ref=\"G4_W\"/>\n"
out+="\t\t<fraction n=\"0.015\" ref=\"G4_Cu\"/>\n"
out+="\t\t<fraction n=\"0.035\" ref=\"G4_Ni\"/>\n"
out+="\t</material>\n"
out+="</materials>\n"



out+="\n\n<solids>\n"



f=open(output_file+".gdml", "w+")


out="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
out+="<gdml\n"
out+="\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
out+="\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n"
out+="\n\n<define>"
out+="\n</define>"

out+="\n\n<solids>\n"

xoff={}
yoff={}
xoff["C"]=0
xoff["outer_E"]= p["E_dy"]
xoff["inner_E"]= -p["C_dx"]
yoff["C"]=0
yoff["outer_E"]= p["E_dy"]
yoff["inner_E"]= 0
for i in ["C", "outer_E","inner_E"]: 
  out+="\n\t<xtru name=\"solid_"+i+"_mid\"  lunit=\"mm\">"
  out+="\n\t\t<twoDimVertex x=\""+str(xoff[i]+ p["C_x2_up"]-p["C_rpos"])+"\" y=\""+str(p["C_z2_up"]-p["C_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(xoff[i]+ p["C_x1_up"]-p["C_rpos"])+"\" y=\""+str(p["C_z1_up"]-p["C_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(-xoff[i]+ p["C_x1_low"]-p["C_rpos"])+"\" y=\""+str(p["C_z1_low"]-p["C_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(-xoff[i]+ p["C_x2_low"]-p["C_rpos"])+"\" y=\""+str(p["C_z2_low"]-p["C_z1_up"])+"\" />"
  out+="\n\t\t<section zOrder=\"1\" zPosition=\""+str(-yoff[i]-p["C_dy"]/2)+"\"/>"
  out+="\n\t\t<section zOrder=\"2\" zPosition=\""+str(yoff[i]+p["C_dy"]/2)+"\"/>"
  out+="\n\t</xtru>"
  out+="\n\t<tube name=\"solid_"+i+"_front\" rmin=\"0\" rmax=\""+str(xoff[i]+p["C_rad_front"])+"\" z=\""+str(2*yoff[i]+p["C_dy"])+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
  out+="\n\t<tube name=\"solid_"+i+"_back\" rmin=\"0\" rmax=\""+str(xoff[i]+p["C_rad_back"])+"\" z=\""+str(2*yoff[i]+p["C_dy"])+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
 
  ### Making unions
  out+="\n\t<multiUnion name=\"solid_"+i+"\">"
  out+="\n\t\t<multiUnionNode name=\"node_solid_"+i+"_front\">"
  out+="\n\t\t\t<solid ref=\"solid_"+i+"_front\"/>"
  out+="\n\t\t\t<position name=\"pos_"+i+"_front\" x=\"0\" y=\"0\" z=\""+str(-p["C_l_arm"]/2)+"\"/>"
  out+="\n\t\t\t<rotation name=\"rot_"+i+"_front\" x=\"3*pi/2\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>"
  out+="\n\t\t<multiUnionNode name=\"node_solid_"+i+"_mid\">"
  out+="\n\t\t\t<solid ref=\"solid_"+i+"_mid\"/>"
  out+="\n\t\t\t<position name=\"pos_"+i+"_mid\" x=\"0\" y=\"0\" z=\""+str(-p["C_l_arm"]/2)+"\"/>"
  out+="\n\t\t\t<rotation name=\"rot_"+i+"_mid\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>"
  out+="\n\t\t<multiUnionNode name=\"node_solid_"+i+"_back\">"
  out+="\n\t\t\t<solid ref=\"solid_"+i+"_back\"/>"
  out+="\n\t\t\t<position name=\"pos_"+i+"_back\" x=\""+str(p["C_x2_up"]-p["C_rad_back"]-p["C_rpos"])+"\" y=\"0\" z=\""+str(p["C_l_arm"]/2)+"\"/>"
  out+="\n\t\t\t<rotation name=\"rot_"+i+"_back\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>\n"
  out+="\n\t</multiUnion>\n"


### Upstream toroid mother
out+="\n\t<tube name=\"solid_US_toroidMother\" rmin=\""+str(r_inner_mother)+"\"  rmax=\""+str(r_outer_mother)+"\" z=\""+str(l_mother)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n"


out+="\n</solids>\n"

out+="\n\n<structure>\n"

for i in range(1,8):
   ### Setting up coils
        out+="\n\t<volume name=\"logic_inner_E_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cu\"/>"
        out+="\n\t\t<solidref ref=\"solid_inner_E\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"orange\"/>"
        out+="\n\t\t<auxiliary auxtype=\"SensDet\" auxvalue=\"coilDet\"/>"
        out+="\n\t\t<auxiliary auxtype=\"DetNo\" auxvalue=\""+str(4007+i)+"\"/>"
        out+="\n\t</volume>\n"

        out+="\n\t<volume name=\"logic_C_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cu\"/>"
        out+="\n\t\t<solidref ref=\"solid_C\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"magenta\"/>"
        out+="\n\t\t<auxiliary auxtype=\"SensDet\" auxvalue=\"coilDet\"/>"
        out+="\n\t\t<auxiliary auxtype=\"DetNo\" auxvalue=\""+str(4000+i)+"\"/>"
        out+="\n\t\t\t<physvol name=\"inner_E\">"
        out+="\n\t\t\t\t<volumeref ref=\"logic_inner_E_"+str(i)+"\"/>"
        out+="\n\t\t\t\t<rotation name=\"rot_inner_E\" y=\"0\" aunit=\"rad\" />"
        out+="\n\t\t\t</physvol>\n"
        out+="\n\t</volume>\n"

        out+="\n\t<volume name=\"logic_outer_E_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cu\"/>"
        out+="\n\t\t<solidref ref=\"solid_outer_E\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"orange\"/>"
        out+="\n\t\t<auxiliary auxtype=\"SensDet\" auxvalue=\"coilDet\"/>"
        out+="\n\t\t<auxiliary auxtype=\"DetNo\" auxvalue=\""+str(4007+i)+"\"/>"
        out+="\n\t\t\t<physvol name=\"C\">"
        out+="\n\t\t\t\t<volumeref ref=\"logic_C_"+str(i)+"\"/>"
        out+="\n\t\t\t</physvol>\n"
        out+="\n\t</volume>\n"


out+="\n\t<volume name=\"US_toroidMother\">"
out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
out+="\n\t\t<solidref ref=\"solid_US_toroidMother\"/>"
out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"

for i in range(1,2):
        rpos=p["C_rpos"]
        theta=2*(i-1)*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta))
        zpos= p["C_zpos"]
        out+="\n\t\t<physvol name=\"ucoil_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_outer_E_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_ucoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\""+str(zpos)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_ucoil_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-theta)+"\"/>"
        out+="\n\t\t</physvol>\n"

out+="\n\t</volume>\n"
out+="\n</structure>\n"



out+="\n<setup name=\"US_toroidWorld\" version=\"1.0\">"
out+="\n\t<world ref=\"US_toroidMother\"/>"
out+="\n</setup>\n"

out+="\n</gdml>"

f.write(out)

