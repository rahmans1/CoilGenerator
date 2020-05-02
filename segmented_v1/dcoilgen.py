#!/usr/bin/env python
import csv
import sys
import os
import subprocess
import math
import time
import argparse



parser= argparse.ArgumentParser(description="Generate a segmented coil based on given parameters")
parser.add_argument("-l", dest="par_list", action="store", required=False, help="Provide the list of parameters. This is different for each of the coil types.")
parser.add_argument("-f", dest="output_file", action="store", required=False, default="DSToroid.gdml", help="Provide the required output file location")

args=parser.parse_args()
output_file=os.path.realpath(args.output_file)


p={}    # dictionary of parameter values

with open(args.par_list) as csvfile:
     reader=csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in reader:
         p[row[0]]=float(row[1])



# segment 1,2,3 
for i in range(1,4):
  p["C"+str(i)+"_l_arm"]= p["C"+str(i)+"_z2_up"]-p["C"+str(i)+"_z1_up"]
  p["C"+str(i)+"_rad_front"]= (p["C"+str(i)+"_x1_up"]-p["C"+str(i)+"_x1_low"])/2.0
  p["C"+str(i)+"_rad_back"]= (p["C"+str(i)+"_x2_up"]-p["C"+str(i)+"_x2_low"])/2.0
  p["C"+str(i)+"_h"]=2*p["C"+str(i)+"_rad_front"]   # fix me
  p["C"+str(i)+"_l"]= p["C"+str(i)+"_l_arm"]+p["C"+str(i)+"_rad_front"]+p["C"+str(i)+"_rad_back"]
  p["C"+str(i)+"_w"]= p["C"+str(i)+"_dy"]
  p["C"+str(i)+"_rpos"]=p["C"+str(i)+"_x1_low"]+ p["C"+str(i)+"_rad_front"]
  p["C"+str(i)+"_zpos"]=p["C"+str(i)+"_z1_up"]+p["C"+str(i)+"_l_arm"]/2-13000


# segment 4
for j in ["tb", "mid"]:
  p["C4_"+j+"_l_arm"]= p["C4_"+j+"_z2_up"]-p["C4_"+j+"_z1_up"]
  p["C4_"+j+"_rad_front"]= (p["C4_"+j+"_x1_up"]-p["C4_"+j+"_x1_low"])/2.0
  p["C4_"+j+"_rad_back"]= (p["C4_"+j+"_x2_up"]-p["C4_"+j+"_x2_low"])/2.0
  p["C4_"+j+"_rpos"]=p["C4_"+j+"_x1_low"]+ p["C4_"+j+"_rad_front"]
  p["C4_"+j+"_zpos"]=p["C4_"+j+"_z1_up"]+p["C4_"+j+"_l_arm"]/2-13000


p["C4_w"]= 2*p["C4_tb_dy"]+2*p["C4_mid_dy"]+2*p["E_tb_dy"]+2*p["E_mid_dy"]+2*p["E_dy"]

r_inner_mother=38
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

for i in range(1,4):
  out+="\n\t<xtru name=\"solid_C"+str(i)+"_mid\"  lunit=\"mm\">"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C"+str(i)+"_x2_up"]-p["C"+str(i)+"_rpos"])+"\" y=\""+str(p["C"+str(i)+"_z2_up"]-p["C"+str(i)+"_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C"+str(i)+"_x1_up"]-p["C"+str(i)+"_rpos"])+"\" y=\""+str(p["C"+str(i)+"_z1_up"]-p["C"+str(i)+"_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C"+str(i)+"_x1_low"]-p["C"+str(i)+"_rpos"])+"\" y=\""+str(p["C"+str(i)+"_z1_low"]-p["C"+str(i)+"_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C"+str(i)+"_x2_low"]-p["C"+str(i)+"_rpos"])+"\" y=\""+str(p["C"+str(i)+"_z2_low"]-p["C"+str(i)+"_z1_up"])+"\" />"
  out+="\n\t\t<section zOrder=\"1\" zPosition=\""+str(-p["C"+str(i)+"_dy"]/2)+"\"/>"
  out+="\n\t\t<section zOrder=\"2\" zPosition=\""+str(p["C"+str(i)+"_dy"]/2)+"\"/>"
  out+="\n\t</xtru>"
  out+="\n\t<tube name=\"solid_C"+str(i)+"_front\" rmin=\"0\" rmax=\""+str(p["C"+str(i)+"_rad_front"])+"\" z=\""+str(p["C"+str(i)+"_dy"])+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
  out+="\n\t<tube name=\"solid_C"+str(i)+"_back\" rmin=\"0\" rmax=\""+str(p["C"+str(i)+"_rad_back"])+"\" z=\""+str(p["C"+str(i)+"_dy"])+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
 
  ### Making unions

  out+="\n\t<multiUnion name=\"solid_C"+str(i)+"\">"
  out+="\n\t\t<multiUnionNode name=\"node_solid_C"+str(i)+"_front\">"
  out+="\n\t\t\t<solid ref=\"solid_C"+str(i)+"_front\"/>"
  out+="\n\t\t\t<position name=\"pos_C"+str(i)+"_front\" x=\"0\" y=\"0\" z=\""+str(-p["C"+str(i)+"_l_arm"]/2)+"\"/>"
  out+="\n\t\t\t<rotation name=\"rot_C"+str(i)+"_front\" x=\"3*pi/2\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>"
  out+="\n\t\t<multiUnionNode name=\"node_solid_C"+str(i)+"_mid\">"
  out+="\n\t\t\t<solid ref=\"solid_C"+str(i)+"_mid\"/>"
  out+="\n\t\t\t<position name=\"pos_C"+str(i)+"_mid\" x=\"0\" y=\"0\" z=\""+str(-p["C"+str(i)+"_l_arm"]/2)+"\"/>"
  out+="\n\t\t\t<rotation name=\"rot_C"+str(i)+"_mid\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>"
  out+="\n\t\t<multiUnionNode name=\"node_solid_C"+str(i)+"_back\">"
  out+="\n\t\t\t<solid ref=\"solid_C"+str(i)+"_back\"/>"
  out+="\n\t\t\t<position name=\"pos_C"+str(i)+"_back\" x=\""+str(p["C"+str(i)+"_x2_up"]-p["C"+str(i)+"_rad_back"]-p["C"+str(i)+"_rpos"])+"\" y=\"0\" z=\""+str(p["C"+str(i)+"_l_arm"]/2)+"\"/>"
  out+="\n\t\t\t<rotation name=\"rot_C"+str(i)+"_back\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>\n"
  out+="\n\t</multiUnion>\n"

  ### individual coil mother
  out+="\n\t<box name=\"solid_DScoil_"+str(i)+"\" lunit=\"mm\" x=\""+str(p["C"+str(i)+"_h"])+"\" y=\""+str(p["C"+str(i)+"_w"])+"\" z=\""+str(p["C"+str(i)+"_l"])+"\"/>"


"""
for j in ["tb", "mid"]:
  out+="\n\t<xtru name=\"solid_C4_"+j+"_mid\"  lunit=\"mm\">"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C4_"+j+"_x2_up"]-p["C4_"+j+"_rpos"])+"\" y=\""+str(p["C4_"+j+"_z2_up"]-p["C4_"+j+"_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C4_"+j+"_x1_up"]-p["C4_"+j+"_rpos"])+"\" y=\""+str(p["C4_"+j+"_z1_up"]-p["C4_"+j+"_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C4_"+j+"_x1_low"]-p["C4_"+j+"_rpos"])+"\" y=\""+str(p["C4_"+j+"_z1_low"]-p["C4_"+j+"_z1_up"])+"\" />"
  out+="\n\t\t<twoDimVertex x=\""+str(p["C4_"+j+"_x2_low"]-p["C4_"+j+"_rpos"])+"\" y=\""+str(p["C4_"+j+"_z2_low"]-p["C4_"+j+"_z1_up"])+"\" />"
  out+="\n\t\t<section zOrder=\"1\" zPosition=\""+str(-p["C4_"+j+"_dy"]/2)+"\"/>"
  out+="\n\t\t<section zOrder=\"2\" zPosition=\""+str(p["C4_"+j+"_dy"]/2)+"\"/>"
  out+="</xtru>\n"
  out+="\n\t<tube name=\"solid_C4_"+j+"_front\" rmin=\"0\" rmax=\""+str(p["C4_"+j+"_rad_front"])+"\" z=\""+str(p["C4_"+j+"_dy"])+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"
  out+="\n\t<tube name=\"solid_C4_"+j+"_back\" rmin=\"0\" rmax=\""+str(p["C4_"+j+"_rad_back"])+"\" z=\""+str(p["C4_"+j+"_dy"])+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"

  ### Making unions

  out+="\n\t<multiUnion name=\"solid_C4_"+j+"\">"
  out+="\n\t\t<multiUnionNode name=\"node_solid_C4_"+j+"_front\">"
  out+="\n\t\t\t<solid ref=\"solid_C4_"+j+"_front\"/>"
  out+="\n\t\t\t<position name=\"pos_C4_"+j+"_front\" x=\"0\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t\t<rotation name=\"rot_C4_"+j+"_front\" x=\"0\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>"
  out+="\n\t\t<multiUnionNode name=\"node_solid_C4_"+j+"_mid\">"
  out+="\n\t\t\t<solid ref=\"solid_C4_"+j+"_mid\"/>"
  out+="\n\t\t\t<position name=\"pos_C4_"+j+"_mid\" x=\"0\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t\t<rotation name=\"rot_C4_"+j+"_mid\" x=\"pi\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>"
  out+="\n\t\t<multiUnionNode name=\"node_solid_C4_"+j+"_back\">"
  out+="\n\t\t\t<solid ref=\"solid_C4_"+j+"_back\"/>"
  out+="\n\t\t\t<position name=\"pos_C4_"+j+"_back\" x=\""+str(p["C4_"+j+"_x2_up"]-p["C4_"+j+"_rad_back"]-p["C4_"+j+"_rpos"])+"\" y=\""+str(-p["C4_"+j+"_l_arm"])+"\" z=\"0\"/>"
  out+="\n\t\t\t<rotation name=\"rot_C4_"+j+"_back\" x=\"pi\" y=\"0\" z=\"0\"/>"
  out+="\n\t\t</multiUnionNode>\n"
  out+="\n\t</multiUnion>\n"

"""

  

"""
out+="\n\t<scaledSolid name=\"scaled_solid_C4\">"
out+="\n\t\t<solidref ref=\"solid_C4\"/>"
out+="\n\t\t<scale name=\"solid_C4_scale\" x=\"2\" y=\"2\" z=\"2\"/>"
out+="\n\t</scaledSolid>\n"
"""


### hybrid toroid mother
out+="\n\t<tube name=\"solid_DS_toroidMother\" rmin=\""+str(r_inner_mother)+"\"  rmax=\""+str(r_outer_mother)+"\" z=\""+str(l_mother)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n"


out+="\n</solids>\n"

out+="\n\n<structure>\n"

for i in range(1,8):
   for j in range(1,4):
        out+="\n\t<volume name=\"logic_DScoil_"+str(j)+"_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cu\"/>"
        out+="\n\t\t<solidref ref=\"solid_C"+str(j)+"\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"magenta\"/>"
        out+="\n\t\t<auxiliary auxtype=\"SensDet\" auxvalue=\"coilDet\"/>"
        out+="\n\t\t<auxiliary auxtype=\"DetNo\" auxvalue=\""+str(3000+i)+"\"/>"
        out+="\n\t</volume>\n"

"""
        out+="\n\t<volume name=\"logic_DScoil_"+str(j)+"_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
        out+="\n\t\t<solidref ref=\"solid_DScoil_"+str(j)+"\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"
        out+="\n\t\t<physvol name=\"C"+str(j)+"_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_C"+str(j)+"_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_C"+str(j)+"\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\""+str(-p["C"+str(j)+"_l_arm"]/2)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_C"+str(j)+"\" x=\"pi/2\" y=\"0\" z=\""+str(0)+"\"/>"
        out+="\n\t\t</physvol>"
        out+="\n\t</volume>\n"
"""

out+="\n\t<volume name=\"DS_toroidMother\">"
out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
out+="\n\t\t<solidref ref=\"solid_DS_toroidMother\"/>"
out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"

for i in range(1,8):
    for j in range(1,4):
        rpos=p["C"+str(j)+"_rpos"]
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta))
        zpos= p["C"+str(j)+"_zpos"]
        out+="\n\t\t<physvol name=\"DScoil_"+str(j)+"_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_DScoil_"+str(j)+"_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_DScoil_"+str(j)+"_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\""+str(zpos)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_DScoil_"+str(j)+"_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-theta)+"\"/>"
        out+="\n\t\t</physvol>\n"


out+="\n\t</volume>\n"
out+="\n</structure>\n"



out+="\n<setup name=\"DS_toroidWorld\" version=\"1.0\">"
out+="\n\t<world ref=\"DS_toroidMother\"/>"
out+="\n</setup>\n"

out+="\n</gdml>"

f.write(out)

