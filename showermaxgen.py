import csv
import sys
import os
import math

output_file="showerMaxGen"

####    radial extent

length_quartz=160.0
length_tungsten=length_quartz
length_mirror_box_tungstenquartz=length_quartz

###  thickness

thick_quartz=10.0
thick_tungsten=8.0
thick_mirror_box_tungstenquartz=4*(thick_quartz+thick_tungsten)

###  width

width_quartz=265.0#238.0#246.888 # must be float
width_tungsten=width_quartz
width_mirror_box_tungstenquartz=width_quartz

### wall parameter

thick_wall_mirror_box_tungstenquartz= 3.302


detector_tilt= 0; #math.pi/3

quartz_rotate=["pi/2", "-pi/2", "pi/2", "-pi/2"]

### mirror parameter

length_mirror_box_bot=82.296
thick_mirror_box_bot=thick_mirror_box_tungstenquartz+2*46.941

pmt_radius= 38.1 ### Radius of 1.5 inches

pmt_window_extent = 3.0
pmt_cathode_extent = 3e-6


thick_mirror_box_top=47.398      # 1.87 inches

length_mirror_box_top=math.sqrt(184.404*184.404-   math.pow((thick_mirror_box_bot-thick_mirror_box_top)/2,2))

length_mirror_box_top=120.0/160.0*length_mirror_box_top
length_mirror_box_bot=120.0/160.0*length_mirror_box_bot


length_logic_mirror_box=length_mirror_box_bot+length_mirror_box_top+pmt_window_extent+pmt_cathode_extent
print(length_mirror_box_bot)
print(length_mirror_box_top)
print(932.5+length_quartz+length_logic_mirror_box)



zstagger=(thick_mirror_box_bot+2.0*thick_wall_mirror_box_tungstenquartz)/2-36.243-10 # FIX ME: Hard Code this and chcheck for overlaps
print(zstagger)
print(24498-2*(thick_quartz+thick_tungsten)+zstagger)
print(24498-2*(thick_quartz+thick_tungsten)-zstagger)

len_mother=2*thick_mirror_box_bot+2*zstagger+5

z_origin = 0
pos=1020.0+length_quartz/2

f=open(output_file+".gdml", "w+")

out="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
out+="<gdml"
out+="\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
out+="\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n"
out+="\n\n<define>"
out+="\n</define>"


out+="\n\n<solids>\n"

out+="\t<tube name=\"solid_pmt_window\" rmin=\"0\" rmax=\""+str(pmt_radius)+"\" z=\""+str(pmt_window_extent)+"\" deltaphi=\"2*pi\" startphi=\"0\" aunit=\"rad\" lunit=\"mm\"/>\n"

out+="\t<tube name=\"solid_pmt_cathode\" rmin=\"0\" rmax=\""+str(pmt_radius)+"\" z=\""+str(pmt_cathode_extent)+"\" deltaphi=\"2*pi\" startphi=\"0\" aunit=\"rad\" lunit=\"mm\"/>\n"

out+="\t<box name=\"solid_mirror_box_tungstenquartz_1\" lunit=\"mm\" x=\""+str(length_mirror_box_tungstenquartz)+"\" y=\""+str(width_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\" z=\""+str(thick_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\"/>\n"

out+="\t<box name=\"solid_mirror_box_tungstenquartz_2\" lunit=\"mm\" x=\""+str(length_mirror_box_tungstenquartz+1)+"\" y=\""+str(width_mirror_box_tungstenquartz)+"\" z=\""+str(thick_mirror_box_tungstenquartz)+"\"/>\n"

out+="\t<subtraction name=\"solid_mirror_box_tungstenquartz\">"
out+="\n\t\t<first ref=\"solid_mirror_box_tungstenquartz_1\"/>"
out+="\n\t\t<second ref=\"solid_mirror_box_tungstenquartz_2\"/>"
out+="\n\t\t<position name=\"pos_subtract_mirror_box_tungstenquartz_12\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_subtract_mirror_box_tungstenquartz_12\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</subtraction>\n"

out+="\t<trd name=\"solid_mirror_box_bot_1\" lunit=\"mm\" x1=\""+str(thick_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\"  x2=\""+str(thick_mirror_box_bot+2*thick_wall_mirror_box_tungstenquartz)+"\" y1=\""+str(width_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\"  y2=\""+str(width_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\" z=\""+str(length_mirror_box_bot)+"\"/>\n"

out+="\t<trd name=\"solid_mirror_box_bot_2\" lunit=\"mm\" x1=\""+str(thick_mirror_box_tungstenquartz)+"\"  x2=\""+str(thick_mirror_box_bot)+"\" y1=\""+str(width_mirror_box_tungstenquartz)+"\"  y2=\""+str(width_mirror_box_tungstenquartz)+"\" z=\""+str(length_mirror_box_bot+1)+"\"/>\n"

out+="\t<subtraction name=\"solid_mirror_box_bot\">"
out+="\n\t\t<first ref=\"solid_mirror_box_bot_1\"/>"
out+="\n\t\t<second ref=\"solid_mirror_box_bot_2\"/>"
out+="\n\t\t<position name=\"pos_subtract_mirror_box_bot_12\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_subtract_mirror_box_bot_12\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</subtraction>\n"

out+="\t<trd name=\"solid_mirror_box_top_1\" lunit=\"mm\" x1=\""+str(thick_mirror_box_bot+2*thick_wall_mirror_box_tungstenquartz)+"\"  x2=\""+str(thick_mirror_box_top+2*thick_wall_mirror_box_tungstenquartz)+"\" y1=\""+str(width_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\"  y2=\""+str(thick_mirror_box_top+2*thick_wall_mirror_box_tungstenquartz)+"\" z=\""+str(length_mirror_box_top)+"\"/>\n"

out+="\t<trd name=\"solid_mirror_box_top_2\" lunit=\"mm\" x1=\""+str(thick_mirror_box_tungstenquartz)+"\"  x2=\""+str(thick_mirror_box_top)+"\" y1=\""+str(width_mirror_box_tungstenquartz)+"\"  y2=\""+str(thick_mirror_box_top)+"\" z=\""+str(length_mirror_box_top+1)+"\"/>\n"

out+="\t<subtraction name=\"solid_mirror_box_top\">"
out+="\n\t\t<first ref=\"solid_mirror_box_top_1\"/>"
out+="\n\t\t<second ref=\"solid_mirror_box_top_2\"/>"
out+="\n\t\t<position name=\"pos_subtract_mirror_box_top_12\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_subtract_mirror_box_top_12\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</subtraction>\n"

out+="\t<xtru name=\"solid_quartz\" lunit=\"mm\">\n"
out+="\t\t<twoDimVertex x=\""+str(-length_quartz/2)+"\" y=\""+str(thick_quartz/2)+"\"/>\n"
out+="\t\t<twoDimVertex x=\""+str(-length_quartz/2)+"\" y=\""+str(-thick_quartz/2)+"\"/>\n"
out+="\t\t<twoDimVertex x=\""+str(length_quartz/2+thick_quartz)+"\" y=\""+str(-thick_quartz/2)+"\"/>\n"
out+="\t\t<twoDimVertex x=\""+str(length_quartz/2)+"\" y=\""+str(thick_quartz/2)+"\"/>\n"
out+="\t\t<section zOrder=\"1\" zPosition=\""+str(-width_quartz/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\"/>\n"
out+="\t\t<section zOrder=\"2\" zPosition=\""+str(width_quartz/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\"/>\n"
out+="\t</xtru>\n"

out+="\t<box name=\"solid_tungsten\" lunit=\"mm\" x=\""+str(length_tungsten)+"\" y=\""+str(width_tungsten)+"\" z=\""+str(thick_tungsten)+"\"/>\n"


out+="\t<box name=\"solid_logic_mirror_box\" lunit=\"mm\" x=\""+str(length_logic_mirror_box)+"\" y=\""+str(width_mirror_box_tungstenquartz+2*thick_wall_mirror_box_tungstenquartz)+"\" z=\""+str(thick_mirror_box_bot+2*thick_wall_mirror_box_tungstenquartz)+"\"/>\n"


out+="\t<union name=\"solid_logic_mirror_box_union\">"
out+="\n\t\t<first ref=\"solid_mirror_box_tungstenquartz_1\"/>"
out+="\n\t\t<second ref=\"solid_logic_mirror_box\"/>"
out+="\n\t\t<position name=\"pos_logic_mirror_box_union\" x=\""+str(length_quartz/2.0+length_logic_mirror_box/2.0)+"\" y=\""+str(0)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_logic_mirror_box_union\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"




out+="\t<cone name=\"solid_showerMaxMother\" rmin1=\""+str(700)+"\"  rmax1=\""+str(1900)+"\" rmin2=\""+str(700)+"\" rmax2=\""+str(1900)+"\"  z=\""+str(len_mother)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n" #Make sure this mother volume doesn't interfere with coils
out+="</solids>\n"


out+="\n\n<materials>\n"
out+="\t<material name=\"G4_Quartz\" state=\"solid\">\n"
out+="\t\t<MEE unit=\"eV\" value=\"139.2\"/>\n"
out+="\t\t<D value=\"2.2\" unit=\"g/cm3\"/>\n"
out+="\t\t<fraction n=\"0.467465468463971\" ref=\"G4_Si\"/>\n"
out+="\t\t<fraction n=\"0.532534531536029\" ref=\"G4_O\"/>\n"
out+="\t</material>\n"

out+="\t<material name=\"G4_Cathode\" state=\"solid\">\n"
#out+="\t\t<MEE unit=\"eV\" value=\"380.1876\"/>\n"
out+="\t\t<D value=\"0.8223\" unit=\"g/cm3\"/>\n"
out+="\t\t<fraction n=\"0.2349\" ref=\"G4_K\"/>\n"
out+="\t\t<fraction n=\"0.3993\" ref=\"G4_Cs\"/>\n"
out+="\t\t<fraction n=\"0.3658\" ref=\"G4_Sb\"/>\n"
out+="\t</material>\n"

out+="</materials>\n"






out+="\n\n<structure>\n"


for i in range(0,28):
        out+="\t<volume name=\"logic_mirror_box_tungstenquartz_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Al\"/>"
        out+="\n\t\t<solidref ref=\"solid_mirror_box_tungstenquartz\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"green\"/>"
        out+="\n\t</volume>\n"

        out+="\t<volume name=\"logic_mirror_box_bot_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Al\"/>"
        out+="\n\t\t<solidref ref=\"solid_mirror_box_bot\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"green\"/>"
        out+="\n\t</volume>\n"

        out+="\t<volume name=\"logic_mirror_box_top_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Al\"/>"
        out+="\n\t\t<solidref ref=\"solid_mirror_box_top\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"green\"/>"
        out+="\n\t</volume>\n"


        out+="\t<volume name=\"logic_pmt_window_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Quartz\"/>"
        out+="\n\t\t<solidref ref=\"solid_pmt_window\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"blue\"/>"
        out+="\n\t</volume>\n"

        out+="\t<volume name=\"logic_pmt_cathode_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cathode\"/>"
        out+="\n\t\t<solidref ref=\"solid_pmt_cathode\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"green\"/>"
        out+="\n\t</volume>\n"


	for j in range(0,4):
        	out+="\t<volume name=\"logic_quartz_"+str(i)+"_"+str(j)+"\">"
        	out+="\n\t\t<materialref ref=\"G4_Quartz\"/>"
        	out+="\n\t\t<solidref ref=\"solid_quartz\"/>"
        	out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"blue\"/>"
                out+="\n\t</volume>\n"
        
                out+="\t<volume name=\"logic_tungsten_"+str(i)+"_"+str(j)+"\">"
                out+="\n\t\t<materialref ref=\"G4_W\"/>"
                out+="\n\t\t<solidref ref=\"solid_tungsten\"/>"
                out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"red\"/>"
                out+="\n\t</volume>\n"


            
        out+="\t<volume name=\"logic_singledet_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_AIR\"/>"
        out+="\n\t\t<solidref ref=\"solid_logic_mirror_box_union\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"


#        out+="\n\t\t<physvol name=\"mirror_box_tungstenquartz_"+str(i)+"\">"
#        out+="\n\t\t\t<volumeref ref=\"logic_mirror_box_tungstenquartz_"+str(i)+"\"/>"
#        out+="\n\t\t\t<position name=\"pos_logic_mirror_box_tungstenquartz_"+str(i)+"\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\""+str(0)+"\"/>"
#        out+="\n\t\t\t<rotation name=\"rot_logic_mirror_box_tungstenquartz_"+str(i)+"\" x=\""+str(0)+"\" y=\"0\" z=\"0\"/>"
#       out+="\n\t\t</physvol>"


        out+="\n\t\t<physvol name=\"mirror_box_bot_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_mirror_box_bot_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_logic_mirror_box_bot_"+str(i)+"\" x=\""+str(length_quartz/2+length_mirror_box_bot/2)+"\" y=\""+str(0)+"\" z=\""+str(0)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_logic_mirror_box_bot_"+str(i)+"\" x=\""+str(0)+"\" y=\"-pi/2\" z=\"0\"/>"
        out+="\n\t\t</physvol>"

        out+="\n\t\t<physvol name=\"mirror_box_top_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_mirror_box_top_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_logic_mirror_box_top_"+str(i)+"\" x=\""+str(length_quartz/2+length_mirror_box_bot+length_mirror_box_top/2)+"\" y=\""+str(0)+"\" z=\""+str(0)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_logic_mirror_box_top_"+str(i)+"\" x=\""+str(0)+"\" y=\"-pi/2\" z=\"0\"/>"
        out+="\n\t\t</physvol>"


        out+="\n\t\t<physvol name=\"pmt_window_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_pmt_window_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_logic_pmt_window_"+str(i)+"\" x=\""+str(length_quartz/2+length_mirror_box_bot+length_mirror_box_top+pmt_window_extent/2)+"\" y=\""+str(0)+"\" z=\""+str(0)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_logic_pmt_window_"+str(i)+"\" x=\""+str(0)+"\" y=\"-pi/2\" z=\"0\"/>"
        out+="\n\t\t</physvol>"

        out+="\n\t\t<physvol name=\"pmt_cathode_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_pmt_cathode_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_logic_pmt_cathode_"+str(i)+"\" x=\""+str(length_quartz/2+length_mirror_box_bot+length_mirror_box_top+pmt_window_extent+pmt_cathode_extent/2)+"\" y=\""+str(0)+"\" z=\""+str(0)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_logic_pmt_cathode_"+str(i)+"\" x=\""+str(0)+"\" y=\"-pi/2\" z=\"0\"/>"
        out+="\n\t\t</physvol>"

        for j in range(0,4):
        	out+="\n\t\t<physvol name=\"quartz_"+str(i)+"_"+str(j)+"\">"
        	out+="\n\t\t\t<volumeref ref=\"logic_quartz_"+str(i)+"_"+str(j)+"\"/>"
        	out+="\n\t\t\t<position name=\"pos_logic_quartz_"+str(i)+"_"+str(j)+"\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\""+str(1.5*thick_quartz+2.0*thick_tungsten-j*(thick_quartz+thick_tungsten))+"\"/>"
        	out+="\n\t\t\t<rotation name=\"rot_logic_quartz_"+str(i)+"_"+str(j)+"\" x=\""+quartz_rotate[j]+"\" y=\"0\" z=\"0\"/>"        
        	out+="\n\t\t</physvol>"


                out+="\n\t\t<physvol name=\"tungsten_"+str(i)+"_"+str(j)+"\">"
                out+="\n\t\t\t<volumeref ref=\"logic_tungsten_"+str(i)+"_"+str(j)+"\"/>"
                out+="\n\t\t\t<position name=\"pos_logic_tungsten_"+str(i)+"_"+str(j)+"\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\""+str(1.5*thick_tungsten+1.0*thick_quartz-j*(thick_quartz+thick_tungsten))+"\"/>"
                out+="\n\t\t\t<rotation name=\"rot_logic_tungsten_"+str(i)+"_"+str(j)+"\" x=\"0\" y=\"0\" z=\"0\"/>"
                out+="\n\t\t</physvol>"

        out+="\n\t</volume>\n"
        

out+="\t<volume name=\"showerMaxMother\">"
out+="\n\t\t<materialref ref=\"G4_AIR\"/>"
out+="\n\t\t<solidref ref=\"solid_showerMaxMother\"/>"
out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"

for i in range(0,28):
        rpos=pos
        theta=math.pi+2*i*math.pi/28
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
        if (i%2==0):	
		zpos=-zstagger
        if (i%2==1):
		zpos=zstagger
	out+="\n\t\t<physvol name=\"singledet_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_singledet_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_singledet_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\""+str(zpos)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_singledet_"+str(i)+"\" x=\""+str(math.asin(-math.sin(theta)*math.sin(detector_tilt)))+"\" y=\""+str(math.asin(math.cos(theta)*math.sin(detector_tilt)))+"\" z=\""+str(-theta)+"\"/>"
        out+="\n\t\t</physvol>"

out+="\n\t</volume>"


out+="\n</structure>\n"

out+="<setup name=\"showerMaxWorld\" version=\"1.0\">"
out+="\n\t<world ref=\"showerMaxMother\"/>"
out+="\n</setup>\n"

out+="</gdml>\n"

f.write(out)















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











