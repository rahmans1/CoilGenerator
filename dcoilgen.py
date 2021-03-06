import csv
import sys
import os
import math

output_file="hybridToroid"
cm=10.0

# segment 1
s1_x=(17.25-14.5)*cm         # extent along x
s1_y=2.7*cm                    # extent along y
s1_l_arm=(1100-1000)*cm      # length of arms
s1_rad=(17.25-4)/2*cm        # arc rad of nose  
s1_theta=math.atan((20.0-17.25)*cm/s1_l_arm)     # slant angle of upper arm

# segment 2
s2_x=(17.25-15.9)*cm 
s2_y=2.7*cm 
s2_l_arm=(1200-1100)*cm                            # length of arms
s2_rad=(s1_rad-s1_x+s1_l_arm/2*math.tan(s1_theta)) # arc rad of nose
s2_theta=math.atan((25.45-20)*cm/s2_l_arm)

# segment 3
s3_x=(21.4-18.65)*cm
s3_y=2.7*cm
s3_l_arm=(1300-1200)*cm
s3_rad=(s2_rad-s2_x+s2_l_arm/2*math.tan(s2_theta))
s3_theta=math.atan((29.1-25.45)*cm/s3_l_arm)

# segment 4
s4_x=s1_x+s2_x+s3_x           # is this correct?
s4_y_tb=1.4*cm                  # thickness of top and bottom pancake
s4_y_mid=2.7*cm                 # thickness of middle pancake
s4_y=2*s4_y_tb+s4_y_mid       # total thickness of segment 4 
s4_l_arm_low1= (1404-1300)*cm # length of low1. low1 is bottom arm adjacent to nose.
s4_l_arm_low2= (1480-1404)*cm # length of low2
s4_theta_low1=math.atan((6.4-4)*cm/s4_l_arm_low1)   #angle of rise of low1.
s4_l_arm_low3= (1656-1480)*cm # length of low3.
s4_theta_low3= math.atan((25.8-14.8)*cm/s4_l_arm_low3) 
s4_l_arm_low4= (1670-1656)*cm # length of low4
s4_theta_low4= math.atan((25.8-25.6)*cm/s4_l_arm_low4)

s4_rad=s3_rad-s3_x+s3_l_arm/2*math.tan(s3_theta)+s4_x-s4_l_arm_low1/2*math.tan(s4_theta_low1) # calculating the radius of front noses of top and bottom pancake


s4_l_arm_up1= (1340-1300)*cm # length of up1. up1 is top arm adjacent to nose.
s4_theta_up1= math.atan((30-22.20)*cm/s4_l_arm_up1) 

s4_l_arm_up2= (1444-1340)*cm
s4_theta_up2= math.atan((33.3-30)*cm/s4_l_arm_up2)

s4_l_arm_up3= (1476-1444)*cm
s4_h_arm_up3= (40.2-20.8)*cm
s4_l_box_up3= (s4_l_arm_up3-s4_h_arm_up3+s4_x)/2
s4_rad_up3= s4_h_arm_up3/2

s4_l_arm_up4= (1656-1476)*cm
s4_theta_up4= math.atan((32.5-20.8)*cm/s4_l_arm_up4)

s4_l_arm_up5= (1670-1656)*cm
s4_theta_up5= math.atan((33.5-32.5)*cm/s4_l_arm_up5)

s4_rad_end_up=s4_rad-s4_h_arm_up3+s4_x+ s4_l_arm_up1*math.tan(s4_theta_up1)+ s4_l_arm_up2*math.tan(s4_theta_up2)+s4_l_arm_up4*math.tan(s4_theta_up4)+s4_l_arm_up5*math.tan(s4_theta_up5)
s4_rad_end_low=-s4_rad+(s4_l_arm_low2)*math.tan(s4_theta_low1)+(s4_l_arm_low3)*math.tan(s4_theta_low3)-(s4_l_arm_low4)*math.tan(s4_theta_low4)
s4_rad_end=(s4_rad_end_up-s4_rad_end_low)/2


h_single_coil=s4_rad_end_up-s4_rad+2*s1_rad+s1_l_arm*math.tan(s1_theta)+s2_l_arm*math.tan(s2_theta)+s3_l_arm*math.tan(s3_theta)

l_single_coil=(s1_rad+s1_l_arm+s2_l_arm+s3_l_arm+s4_l_arm_up1+s4_l_arm_up2+s4_l_arm_up3+s4_l_arm_up4+s4_l_arm_up5+s4_rad_end)
x_origin=s1_rad-h_single_coil/2
z_origin= s1_rad-l_single_coil/2

print("The length of the coil is "+str(l_single_coil)+" and height is "+str(h_single_coil)+" \n")
print("The radius of the front end is "+str(s1_rad)+"\n")
print("The mother volume should be placed at "+str(10000-z_origin)+"\n")

pos=4*cm+h_single_coil/2

r_inner_mother=pos-h_single_coil/2
r_outer_mother=pos+h_single_coil/2+10
l_mother=l_single_coil+20


# photon collimator
r_inner_photon=74.22
r_outer_photon=180.22
r_extent_photon=r_outer_photon-r_inner_photon
h_inner_photon=2*18.25
h_outer_photon=2*54.15
r_inner_sub_photon=116.38
r_extent_sub_photon=r_outer_photon-r_inner_sub_photon
h_inner_sub_photon=2*12.75
h_outer_sub_photon=2*29.15
t_photon=70


f=open(output_file+".gdml", "w+")


out="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
out+="<gdml\n"
out+="\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
out+="\n\txsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n"
out+="\n\n<define>"
out+="\n</define>"


out+="\n\n<materials>\n"
out+="\t<material name=\"G4_CW95\" state=\"solid\">\n"
out+="\t\t<D value=\"18.0\" unit=\"g/cm3\"/>\n"
out+="\t\t<fraction n=\"0.9500\" ref=\"G4_W\"/>\n"
out+="\t\t<fraction n=\"0.015\" ref=\"G4_Cu\"/>\n"
out+="\t\t<fraction n=\"0.035\" ref=\"G4_Ni\"/>\n"
out+="\t</material>\n"
out+="</materials>\n"



out+="\n\n<solids>\n"
out+="\n\t<box name=\"solid_s1_lowerArm\" lunit=\"mm\" x=\""+str(s1_x)+"\" y=\""+str(s1_y)+"\" z=\""+str(s1_l_arm)+"\"/>"
out+="\n\t<para name=\"solid_s1_upperArm\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s1_x)+"\" y=\""+str(s1_y)+"\" z=\""+str(s1_l_arm)+"\" alpha=\"0\" theta=\""+str(s1_theta)+"\" phi=\"0\"/>"
out+="\n\t<tube name=\"solid_s1_frontNose\" rmin=\""+str(s1_rad-s1_x)+"\"  rmax=\""+str(s1_rad)+"\" z=\""+str(s1_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"

out+="\n\t<box name=\"solid_s2_lowerArm\" lunit=\"mm\" x=\""+str(s1_x+s2_x)+"\" y=\""+str(s2_y)+"\" z=\""+str(s2_l_arm)+"\"/>"
out+="\n\t<para name=\"solid_s2_upperArm\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s1_x+s2_x)+"\" y=\""+str(s2_y)+"\" z=\""+str(s2_l_arm)+"\" alpha=\"0\" theta=\""+str(s2_theta)+"\" phi=\"0\"/>"
out+="\n\t<tube name=\"solid_s2_frontNose\" rmin=\""+str(s2_rad-s2_x)+"\"  rmax=\""+str(s2_rad)+"\" z=\""+str(s2_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"

out+="\n\t<box name=\"solid_s3_lowerArm\" lunit=\"mm\" x=\""+str(s1_x+s2_x+s3_x)+"\" y=\""+str(s3_y)+"\" z=\""+str(s3_l_arm)+"\"/>"
out+="\n\t<para name=\"solid_s3_upperArm\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s1_x+s2_x+s3_x)+"\" y=\""+str(s3_y)+"\" z=\""+str(s3_l_arm)+"\" alpha=\"0\" theta=\""+str(s3_theta)+"\" phi=\"0\"/>"
out+="\n\t<tube name=\"solid_s3_frontNose\" rmin=\""+str(s3_rad-s3_x)+"\"  rmax=\""+str(s3_rad)+"\" z=\""+str(s3_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"

out+="\n\t<para name=\"solid_s4_low1_tb\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y_tb)+"\" z=\""+str(s4_l_arm_low1)+"\" alpha=\"0\" theta=\""+str(0)+"\" phi=\"0\"/>"
out+="\n\t<para name=\"solid_s4_low1_mid\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y_mid)+"\" z=\""+str(s4_l_arm_low1)+"\" alpha=\"0\" theta=\""+str(s4_theta_low1)+"\" phi=\"0\"/>"
out+="\n\t<para name=\"solid_s4_low2\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_low2)+"\" alpha=\"0\" theta=\""+str(s4_theta_low1)+"\" phi=\"0\"/>"
out+="\n\t<para name=\"solid_s4_low3\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_low3)+"\" alpha=\"0\" theta=\""+str(s4_theta_low3)+"\" phi=\"0\"/>"
out+="\n\t<para name=\"solid_s4_low4\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_low4)+"\" alpha=\"0\" theta=\""+str(-s4_theta_low4)+"\" phi=\"0\"/>\n"

out+="\n\t<para name=\"solid_s4_up1\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_up1)+"\" alpha=\"0\" theta=\""+str(s4_theta_up1)+"\" phi=\"0\"/>"
out+="\n\t<para name=\"solid_s4_up2\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_up2)+"\" alpha=\"0\" theta=\""+str(s4_theta_up2)+"\" phi=\"0\"/>\n"

out+="\n\t<tube name=\"solid_s4_up3_S\" rmin=\""+str(s4_rad_up3-s4_x)+"\"  rmax=\""+str(s4_rad_up3)+"\" z=\""+str(s4_y)+"\" startphi=\"0\" deltaphi=\"pi/2\" aunit=\"rad\" lunit=\"mm\"/>"
out+="\n\t<box name=\"solid_s4_up3_box\" x=\""+str(s4_x)+"\" y=\""+str(s4_l_box_up3)+"\" z=\""+str(s4_y)+"\"/>\n"

out+="\n\t<union name=\"solid_s4_up3_half\">"
out+="\n\t\t<first ref=\"solid_s4_up3_S\"/>"
out+="\n\t\t<second ref=\"solid_s4_up3_box\"/>"
out+="\n\t\t<position name=\"pos_s4_box_wrt_S\" x=\""+str(s4_rad_up3-s4_x/2)+"\" y=\""+str(-s4_l_box_up3/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s4_box_wrt_S\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_up3\">"
out+="\n\t\t<first ref=\"solid_s4_up3_half\"/>"
out+="\n\t\t<second ref=\"solid_s4_up3_half\"/>"
out+="\n\t\t<position name=\"pos_s4_S\" x=\""+str(0)+"\" y=\""+str(2*s4_rad_up3-s4_x)+"\" z=\""+str(0)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_S\" x=\"pi\" y=\"pi\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<para name=\"solid_s4_up4\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_up4)+"\" alpha=\"0\" theta=\""+str(s4_theta_up4)+"\" phi=\"0\"/>"
out+="\n\t<para name=\"solid_s4_up5\" lunit=\"mm\" aunit=\"rad\" x=\""+str(s4_x)+"\" y=\""+str(s4_y)+"\" z=\""+str(s4_l_arm_up5)+"\" alpha=\"0\" theta=\""+str(s4_theta_up5)+"\" phi=\"0\"/>"
out+="\n\t<tube name=\"solid_s4_frontNose\" rmin=\""+str(s4_rad-s4_x)+"\"  rmax=\""+str(s4_rad)+"\" z=\""+str(s4_y_tb)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>"
out+="\n\t<tube name=\"solid_s4_endNose\" rmin=\""+str(s4_rad_end-s4_x)+"\"  rmax=\""+str(s4_rad_end)+"\" z=\""+str(s4_y)+"\" startphi=\"0\" deltaphi=\"pi\" aunit=\"rad\" lunit=\"mm\"/>\n"



### Making unions

out+="\n\t<union name=\"solid_s1_1\">"
out+="\n\t\t<first ref=\"solid_s1_frontNose\"/>"
out+="\n\t\t<second ref=\"solid_s1_upperArm\"/>"
out+="\n\t\t<position name=\"pos_s1_1\" x=\""+str(s1_rad-s1_x/2+s1_l_arm/2*math.tan(s1_theta))+"\" y=\""+str(-s1_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s1_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s1\">"
out+="\n\t\t<first ref=\"solid_s1_1\"/>"
out+="\n\t\t<second ref=\"solid_s1_lowerArm\"/>"
out+="\n\t\t<position name=\"pos_s1\" x=\""+str(-s1_rad+s1_x/2)+"\" y=\""+str(-s1_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s1\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s2_1\">"
out+="\n\t\t<first ref=\"solid_s2_frontNose\"/>"
out+="\n\t\t<second ref=\"solid_s2_upperArm\"/>"
out+="\n\t\t<position name=\"pos_s2_1\" x=\""+str(s2_rad-s2_x/2+s1_x/2+s2_l_arm/2*math.tan(s2_theta))+"\" y=\""+str(-s2_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s2_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s2\">"
out+="\n\t\t<first ref=\"solid_s2_1\"/>"
out+="\n\t\t<second ref=\"solid_s2_lowerArm\"/>"
out+="\n\t\t<position name=\"pos_s2\" x=\""+str(-s2_rad+s2_x/2-s1_x/2)+"\" y=\""+str(-s2_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s2\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s3_1\">"
out+="\n\t\t<first ref=\"solid_s3_frontNose\"/>"
out+="\n\t\t<second ref=\"solid_s3_upperArm\"/>"
out+="\n\t\t<position name=\"pos_s3_1\" x=\""+str(s3_rad-s3_x/2+(s1_x+s2_x)/2+s3_l_arm/2*math.tan(s3_theta))+"\" y=\""+str(-s3_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s3_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s3\">"
out+="\n\t\t<first ref=\"solid_s3_1\"/>"
out+="\n\t\t<second ref=\"solid_s3_lowerArm\"/>"
out+="\n\t\t<position name=\"pos_s3\" x=\""+str(-s3_rad+s3_x/2-(s1_x+s2_x)/2)+"\" y=\""+str(-s3_l_arm/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s3\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_1\">"
out+="\n\t\t<first ref=\"solid_s4_frontNose\"/>"
out+="\n\t\t<second ref=\"solid_s4_low1_tb\"/>"
out+="\n\t\t<position name=\"pos_s4_1\" x=\""+str(-s4_rad+s4_x/2)+"\" y=\""+str(-s4_l_arm_low1/2)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s4_1\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_2\">"
out+="\n\t\t<first ref=\"solid_s4_1\"/>"
out+="\n\t\t<second ref=\"solid_s4_low1_mid\"/>"
out+="\n\t\t<position name=\"pos_s4_2\" x=\""+str(-s4_rad+s4_x/2-s4_l_arm_low1/2*math.tan(s4_theta_low1))+"\" y=\""+str(-s4_l_arm_low1/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_2\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_3\">"
out+="\n\t\t<first ref=\"solid_s4_2\"/>"
out+="\n\t\t<second ref=\"solid_s4_1\"/>"
out+="\n\t\t<position name=\"pos_s4_3\" x=\""+str(0)+"\" y=\""+str(0)+"\" z=\""+str(-s4_y_tb-s4_y_mid)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_3\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_4\">"
out+="\n\t\t<first ref=\"solid_s4_3\"/>"
out+="\n\t\t<second ref=\"solid_s4_up1\"/>"
out+="\n\t\t<position name=\"pos_s4_4\" x=\""+str(s4_rad-s4_x/2+s4_l_arm_up1/2*math.tan(s4_theta_up1))+"\" y=\""+str(-s4_l_arm_up1/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_4\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_5\">"
out+="\n\t\t<first ref=\"solid_s4_4\"/>"
out+="\n\t\t<second ref=\"solid_s4_up2\"/>"
out+="\n\t\t<position name=\"pos_s4_5\" x=\""+str(s4_rad-s4_x/2+ s4_l_arm_up1*math.tan(s4_theta_up1)+ s4_l_arm_up2/2*math.tan(s4_theta_up2))+"\" y=\""+str(-s4_l_arm_up1-s4_l_arm_up2/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_5\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_6\">"
out+="\n\t\t<first ref=\"solid_s4_5\"/>"
out+="\n\t\t<second ref=\"solid_s4_up3\"/>"
out+="\n\t\t<position name=\"pos_s4_6\" x=\""+str(s4_rad+s4_l_arm_up1*math.tan(s4_theta_up1)+s4_l_arm_up2*math.tan(s4_theta_up2)-s4_rad_up3)+"\" y=\""+str(-s4_l_arm_up1-s4_l_arm_up2-s4_l_box_up3)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_6\" x=\"pi\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_7\">"
out+="\n\t\t<first ref=\"solid_s4_6\"/>"
out+="\n\t\t<second ref=\"solid_s4_low2\"/>"
out+="\n\t\t<position name=\"pos_s4_7\" x=\""+str(-s4_rad+s4_x/2+(s4_l_arm_low2)/2*math.tan(s4_theta_low1))+"\" y=\""+str(-s4_l_arm_low1-s4_l_arm_low2/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_7\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_8\">"
out+="\n\t\t<first ref=\"solid_s4_7\"/>"
out+="\n\t\t<second ref=\"solid_s4_low3\"/>"
out+="\n\t\t<position name=\"pos_s4_8\" x=\""+str(-s4_rad+s4_x/2+(s4_l_arm_low2)*math.tan(s4_theta_low1)+(s4_l_arm_low3)/2*math.tan(s4_theta_low3))+"\" y=\""+str(-s4_l_arm_low1-s4_l_arm_low2-s4_l_arm_low3/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_8\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_9\">"
out+="\n\t\t<first ref=\"solid_s4_8\"/>"
out+="\n\t\t<second ref=\"solid_s4_low4\"/>"
out+="\n\t\t<position name=\"pos_s4_9\" x=\""+str(-s4_rad+s4_x/2+(s4_l_arm_low2)*math.tan(s4_theta_low1)+(s4_l_arm_low3)*math.tan(s4_theta_low3)-(s4_l_arm_low4)/2*math.tan(s4_theta_low4))+"\" y=\""+str(-s4_l_arm_low1-s4_l_arm_low2-s4_l_arm_low3-s4_l_arm_low4/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_9\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_10\">"
out+="\n\t\t<first ref=\"solid_s4_9\"/>"
out+="\n\t\t<second ref=\"solid_s4_up4\"/>"
out+="\n\t\t<position name=\"pos_s4_10\" x=\""+str(s4_rad-s4_h_arm_up3+s4_x/2+ s4_l_arm_up1*math.tan(s4_theta_up1)+ s4_l_arm_up2*math.tan(s4_theta_up2)+s4_l_arm_up4/2*math.tan(s4_theta_up4))+"\" y=\""+str(-s4_l_arm_up1-s4_l_arm_up2-s4_l_arm_up3-s4_l_arm_up4/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_10\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4_11\">"
out+="\n\t\t<first ref=\"solid_s4_10\"/>"
out+="\n\t\t<second ref=\"solid_s4_up5\"/>"
out+="\n\t\t<position name=\"pos_s4_11\" x=\""+str(s4_rad-s4_h_arm_up3+s4_x/2+ s4_l_arm_up1*math.tan(s4_theta_up1)+ s4_l_arm_up2*math.tan(s4_theta_up2)+s4_l_arm_up4*math.tan(s4_theta_up4)+s4_l_arm_up5/2*math.tan(s4_theta_up5))+"\" y=\""+str(-s4_l_arm_up1-s4_l_arm_up2-s4_l_arm_up3-s4_l_arm_up4-s4_l_arm_up5/2)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_11\" x=\"pi/2\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s4\">"
out+="\n\t\t<first ref=\"solid_s4_11\"/>"
out+="\n\t\t<second ref=\"solid_s4_endNose\"/>"
out+="\n\t\t<position name=\"pos_s4_12\" x=\""+str(s4_rad-s4_h_arm_up3+s4_x-s4_rad_end+ s4_l_arm_up1*math.tan(s4_theta_up1)+ s4_l_arm_up2*math.tan(s4_theta_up2)+s4_l_arm_up4*math.tan(s4_theta_up4)+s4_l_arm_up5*math.tan(s4_theta_up5))+"\" y=\""+str(-s4_l_arm_up1-s4_l_arm_up2-s4_l_arm_up3-s4_l_arm_up4-s4_l_arm_up5)+"\" z=\""+str(-(s4_y_tb+s4_y_mid)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s4_12\" x=\"-pi\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"


### Final unions
out+="\n\t<union name=\"solid_s1_s2\">"
out+="\n\t\t<first ref=\"solid_s1\"/>"
out+="\n\t\t<second ref=\"solid_s2\"/>"
out+="\n\t\t<position name=\"pos_s1_s2\" x=\""+str(s1_l_arm/2*math.tan(s1_theta))+"\" y=\""+str(-s1_l_arm)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s1_s2\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s1_s2_s3\">"
out+="\n\t\t<first ref=\"solid_s1_s2\"/>"
out+="\n\t\t<second ref=\"solid_s3\"/>"
out+="\n\t\t<position name=\"pos_s1_s2_s3\" x=\""+str(s1_l_arm/2*math.tan(s1_theta)+s2_l_arm/2*math.tan(s2_theta))+"\" y=\""+str(-s1_l_arm-s2_l_arm)+"\" z=\"0\"/>"
out+="\n\t\t<rotation name=\"rot_s1_s2_s3\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

out+="\n\t<union name=\"solid_s1_s2_s3_s4\">"
out+="\n\t\t<first ref=\"solid_s1_s2_s3\"/>"
out+="\n\t\t<second ref=\"solid_s4\"/>"
out+="\n\t\t<position name=\"pos_s1_s2_s3_s4\" x=\""+str(s1_l_arm/2*math.tan(s1_theta)+s2_l_arm/2*math.tan(s2_theta)+s3_l_arm/2*math.tan(s3_theta)+s4_l_arm_low1/2*math.tan(s4_theta_low1))+"\" y=\""+str(-s1_l_arm-s2_l_arm-s3_l_arm)+"\" z=\""+str((s4_y_mid+s4_y_tb)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_s1_s2_s3_s4\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"



### photon collimator solid
out+="\n\t<xtru name=\"solid_photon_collimator\" lunit=\"mm\">"
out+="\n\t\t<twoDimVertex x=\""+str(-r_extent_photon/2)+"\" y=\""+str(h_inner_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(-r_extent_photon/2)+"\" y=\""+str(-h_inner_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(r_extent_photon/2)+"\" y=\""+str(-h_outer_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(r_extent_photon/2)+"\" y=\""+str(-h_outer_sub_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(r_extent_photon/2-r_extent_sub_photon)+"\" y=\""+str(-h_inner_sub_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(r_extent_photon/2-r_extent_sub_photon)+"\" y=\""+str(h_inner_sub_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(r_extent_photon/2)+"\" y=\""+str(h_outer_sub_photon/2)+"\"/>"
out+="\n\t\t<twoDimVertex x=\""+str(r_extent_photon/2)+"\" y=\""+str(h_outer_photon/2)+"\"/>"
out+="\n\t\t<section zOrder=\"1\" zPosition=\""+str(-t_photon/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\"/>"
out+="\n\t\t<section zOrder=\"2\" zPosition=\""+str(t_photon/2)+"\" xOffset=\"0\" yOffset=\"0\" scalingFactor=\"1\"/>"
out+="\n\t</xtru>\n"

### individual coil mother
out+="\n\t<box name=\"solid_dcoil_mid\" lunit=\"mm\" x=\""+str(h_single_coil)+"\" y=\""+str(s1_y)+"\" z=\""+str(l_single_coil)+"\"/>"
out+="\n\t<box name=\"solid_dcoil_tb\" lunit=\"mm\" x=\""+str(h_single_coil-s4_l_arm_low1*math.tan(s4_theta_low1))+"\" y=\""+str(s4_y)+"\" z=\""+str(l_single_coil-s1_rad-s1_l_arm-s2_l_arm-s3_l_arm+s4_rad)+"\"/>"
out+="\n\t<union name=\"solid_dcoil\">"
out+="\n\t\t<first ref=\"solid_dcoil_mid\"/>"
out+="\n\t\t<second ref=\"solid_dcoil_tb\"/>"
out+="\n\t\t<position name=\"pos_dcoil\" x=\""+str(s4_l_arm_low1/2*math.tan(s4_theta_low1))+"\" y=\""+str(0)+"\" z=\""+str((s1_rad+s1_l_arm+s2_l_arm+s3_l_arm-s4_rad)/2)+"\"/>"
out+="\n\t\t<rotation name=\"rot_dcoil\" x=\"0\" y=\"0\" z=\"0\"/>"
out+="\n\t</union>\n"

### hybrid toroid mother
out+="\n\t<tube name=\"solid_DS_toroidMother\" rmin=\""+str(r_inner_mother)+"\"  rmax=\""+str(r_outer_mother)+"\" z=\""+str(l_mother)+"\" startphi=\"0\" deltaphi=\"360\" aunit=\"deg\" lunit=\"mm\"/>\n"

out+="\n</solids>\n"

out+="\n\n<structure>\n"

for i in range(0,7):
	out+="\n\t<volume name=\"logic_s1_s2_s3_s4_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Cu\"/>"
        out+="\n\t\t<solidref ref=\"solid_s1_s2_s3_s4\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Color\" auxvalue=\"magenta\"/>"
        out+="\n\t\t<auxiliary auxtype=\"SensDet\" auxvalue=\"coilDet\"/>"
        out+="\n\t\t<auxiliary auxtype=\"DetNo\" auxvalue=\""+str(3000+i+1)+"\"/>"
        out+="\n\t</volume>\n"
        
	out+="\n\t<volume name=\"logic_dcoil_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
        out+="\n\t\t<solidref ref=\"solid_dcoil\"/>"
        out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"
        out+="\n\t\t<physvol name=\"s1_s2_s3_s4_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_s1_s2_s3_s4_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_s1_s2_s3_s4_"+str(i)+"\" x=\""+str(x_origin)+"\" y=\""+str(0)+"\" z=\""+str(z_origin)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_s1_s2_s3_s4_"+str(i)+"\" x=\"pi/2\" y=\"0\" z=\""+str(0)+"\"/>"
        out+="\n\t\t</physvol>"
        out+="\n\t</volume>\n"

        out+="\n\t<volume name=\"logic_photon_collimator_"+str(i)+"\">"
        out+="\n\t\t<materialref ref=\"G4_CW95\"/>"
        out+="\n\t\t<solidref ref=\"solid_photon_collimator\"/>"
        out+="\n\t</volume>\n"


out+="\n\t<volume name=\"DS_toroidMother\">"
out+="\n\t\t<materialref ref=\"G4_Galactic\"/>"
out+="\n\t\t<solidref ref=\"solid_DS_toroidMother\"/>"
out+="\n\t\t<auxiliary auxtype=\"Alpha\" auxvalue=\"0.0\"/>"

for i in range(0,7):
        rpos=pos
        theta=2*i*math.pi/7
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta)) 
	out+="\n\t\t<physvol name=\"dcoil_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_dcoil_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_dcoil_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\"0\"/>"
        out+="\n\t\t\t<rotation name=\"rot_dcoil_"+str(i)+"\" x=\"0\" y=\"0\" z=\""+str(-theta)+"\"/>"
        out+="\n\t\t</physvol>\n"

        rpos=r_inner_photon+r_extent_photon/2
        theta=2*i*math.pi/7+2*math.pi/14
        xpos=rpos*(math.cos(theta))
        ypos=rpos*(math.sin(theta))
        zpos=12835-10000-l_single_coil/2+s1_rad

        out+="\n\t\t<physvol name=\"photon_collimator_"+str(i)+"\">"
        out+="\n\t\t\t<volumeref ref=\"logic_photon_collimator_"+str(i)+"\"/>"
        out+="\n\t\t\t<position name=\"pos_photon_collimator_"+str(i)+"\" x=\""+str(xpos)+"\" y=\""+str(ypos)+"\" z=\""+str(zpos)+"\"/>"
        out+="\n\t\t\t<rotation name=\"rot_photon_collimator_"+str(i)+"\" x=\""+str(0)+"\" y=\"0\" z=\""+str(-theta)+"\"/>"
        out+="\n\t\t</physvol>\n"

out+="\n\t</volume>\n"
out+=("\n</structure>\n")


out+="\n<setup name=\"DS_toroidWorld\" version=\"1.0\">"
out+="\n\t<world ref=\"DS_toroidMother\"/>"
out+="\n</setup>\n"

out+="\n</gdml>"

f.write(out)












