# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:22:57 2021

@author: arock
"""
"""
VARS IS THE BEST BUILT IN ATTRIBUTE
use text keyword to get value
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
import shutil as sh

uname = "arock"
BIN = input("Please enter the name of the BIN name in BrR to establish the working directory.  \n\ (The underscore is usually omitted from the BrR filename)\n\nEnter here:")
Span = input("Please enter the span name to establish the working directory.  \n\ne.g.: Girder-Floorbeam-Stringer or Span1, etc.\n\nEnter here:")
Method = input("If this is for LFR, leave this entry blank. Otherwise, enter 'no' \n\nEnter here:")
differentiator = input("Enter a name so you can differentiate runs \n\nEnter here:")
if Method == "":
    Method = "AASHTO_Truss_LFD"
    FileName = "RatingResults"
  
else:
    Method = "AASHTO_Truss_LRFR"
    FileName = "RatingLrfrResults" 
    
Truss = input("If this BIN only has one unique truss (assumed to be named Left Truss), enter 1; otherwise enter 2.\n\nEnter here:")
if Truss == "1":
    Truss = ["LeftTruss"]  
else:
    Truss = ["LeftTruss","RightTruss"]

left = []
right = []
"""
Tags from top to bottom:
    
Detailed_Rating_Results
    Detailed_Results_Table
        Detailed_Truss_Member_Panel_Point_Results
            Detailed_Results_Table
                Detailed_Results_Row
                    Panel_Point
                    Truss_Member_Row
                        Truss_Member
                        Inv_LimitState
                        Inv_RF
                        Op_RF
        Detailed_Panel_Point_Results
            Detailed_Results_Table
                Detailed_Results_Row
                Panel_Point
                Inv_LimitState
                Inv_RF
                Op_RF

""""Span",Span
for truss in Truss:
 
    cwd = r'C:\Users\uname\Documents\AASHTOWARE\BrDR70\BIN\Span\Truss\Method'.replace("\\","/").replace("BIN",BIN).replace("Truss",truss).replace("Span",Span).replace("Method",Method).replace("uname",uname) + "/"
    #create final working directory
    Fwd = r'C:\Users\uname\Documents\AASHTOWARE\BrDR70\BIN\Span'.replace("\\","/").replace("BIN",BIN).replace("Span",Span).replace("uname",uname) + "/"
    tree = ET.parse(cwd+FileName+'.xml')
    root = tree.getroot()
    sh.rmtree(cwd + "Parse_Results/",ignore_errors = True)
    os.mkdir(cwd+"Parse_Results/")
    os.mkdir(cwd+"Parse_Results/Governing/") #create folder for summary results
    os.mkdir(cwd+"Parse_Results/Governing/No_PS/") #create folder for summary results if partial shear is fixed
    
    #for child in root:
    #    print(child.tag, child.attrib)
        
        
    
    if Method == "AASHTO_Truss_LFD":
        detailed_rating_results = [i for i in root.find("Detailed_Truss_Results")]
    else:
        detailed_rating_results = [i for i in root.find("Detailed_Rating_Results")]
    
    numTrucks = len(detailed_rating_results)

    truckNames = [detailed_rating_results[i][0].text for i in range(numTrucks)]
    
    
    # Get Panel Point Member Results for all trucks
    overall_rows_1 = []
    rating_rows_1 = []
    for i in range(numTrucks):
        overall_rows_1.append([])
        rating_rows_1.append([])
        
    # Get Panel Point Member Results for all trucks
    overall_rows_2 = []
    rating_rows_2 = []
    for i in range(numTrucks):
        overall_rows_2.append([])
        rating_rows_2.append([])
    
    for i in range(numTrucks):
        count = 0
        if Method == "AASHTO_Truss_LFD":
            overall_rows_1[i] = detailed_rating_results[i].find("Detailed_Truss_Member_Panel_Point_Results").find("Detailed_Results_Table").findall("Detailed_Results_Row")
        else:
            overall_rows_1[i] = detailed_rating_results[i].find("Detailed_Truss_Member_Panel_Point_Results").findall("Detailed_Results_Row")
        for j in range(len(overall_rows_1[i])):        
            truss_member_rows = overall_rows_1[i][j].findall("Truss_Member_Row")
            for k in range(len(truss_member_rows)):
                rating_rows_1[i].append([])
                rating_rows_1[i][count].append(overall_rows_1[i][j].find("Panel_Point").text)
                rating_rows_1[i][count].append(truss_member_rows[k].find("Truss_Member").text)
                
                if "EV" in truckNames[i]:
                    rating_rows_1[i][count].append(truss_member_rows[k].find("Legal_Op_LimitState").text)                
                    rating_rows_1[i][count].append(truss_member_rows[k].find("Legal_Op_RF").text)
                else:
                    rating_rows_1[i][count].append(truss_member_rows[k].find("Inv_LimitState").text)
                    rating_rows_1[i][count].append(truss_member_rows[k].find("Op_LimitState").text) 
                    rating_rows_1[i][count].append(truss_member_rows[k].find("Inv_RF").text)
                    rating_rows_1[i][count].append(truss_member_rows[k].find("Op_RF").text)
                count +=1
    
    
    for i in range(numTrucks):
        count = 0
        if Method == "AASHTO_Truss_LFD":
            overall_rows_2[i] = detailed_rating_results[i].find("Detailed_Panel_Point_Results").find("Detailed_Results_Table").findall("Detailed_Results_Row")
        else:
            overall_rows_2[i] = detailed_rating_results[i].find("Detailed_Panel_Point_Results").findall("Detailed_Results_Row")
        
        for j in range(len(overall_rows_2[i])):        
            
            rating_rows_2[i].append([])
            rating_rows_2[i][count].append(overall_rows_2[i][j].find("Panel_Point").text)

            if "EV" in truckNames[i]:
                rating_rows_2[i][count].append(overall_rows_2[i][j].find("Legal_Op_LimitState").text)    
                rating_rows_2[i][count].append(overall_rows_2[i][j].find("Legal_Op_RF").text)    
            else:
                                    
                rating_rows_2[i][count].append(overall_rows_2[i][j].find("Inv_LimitState").text)
                rating_rows_2[i][count].append(overall_rows_2[i][j].find("Op_LimitState").text)
                rating_rows_2[i][count].append(overall_rows_2[i][j].find("Inv_RF").text)
                rating_rows_2[i][count].append(overall_rows_2[i][j].find("Op_RF").text)
            count +=1

    
    for j in range(numTrucks):
        outfile1 = cwd+"Parse_Results/"+truckNames[j]+"_"+"Gusset_Ratings"+ ".txt"
        outfile2 = cwd+"Parse_Results/"+truckNames[j]+"_"+"Gusset_PP_Global_Ratings"+ ".txt"
        
        if "EV" not in truckNames[j]:
            fn = open(outfile1,"w")
            
            for i in range(len(rating_rows_1[j])):
                if i == 0:
                    fn.write("Panel_Point"+","+ "Truss_Member"+","+ "Inv_LimitState"+","+ "Op_LimitState"+","+ "Inv_RF"+","+ "Op_RF"+"\n")
                    fn.write(rating_rows_1[j][i][0]+","+ rating_rows_1[j][i][1]+","+ rating_rows_1[j][i][2]+","+ rating_rows_1[j][i][3]+","+ rating_rows_1[j][i][4]+","+ rating_rows_1[j][i][5]+"\n")
                    
                else:
                    fn.write(rating_rows_1[j][i][0]+","+ rating_rows_1[j][i][1]+","+ rating_rows_1[j][i][2]+","+ rating_rows_1[j][i][3]+","+ rating_rows_1[j][i][4]+","+ rating_rows_1[j][i][5]+"\n")
            
            fn.close()
            
            fn2 = open(outfile2,"w")
            
            for i in range(len(rating_rows_2[j])):
                if i == 0:
                    fn2.write("Panel_Point"+","+ "Inv_LimitState"+","+ "Op_LimitState"+","+ "Inv_RF"+","+ "Op_RF"+"\n")
                    fn2.write(rating_rows_2[j][i][0]+","+ rating_rows_2[j][i][1]+","+ rating_rows_2[j][i][2]+","+ rating_rows_2[j][i][3]+","+ rating_rows_2[j][i][4]+"\n")
                    
                else:
                    fn2.write(rating_rows_2[j][i][0]+","+ rating_rows_2[j][i][1]+","+ rating_rows_2[j][i][2]+","+ rating_rows_2[j][i][3]+","+ rating_rows_2[j][i][4]+"\n")
            
            fn2.close()
        
            Data1 = pd.read_csv(outfile1, engine='python')
            subset1 = Data1.loc[Data1['Inv_RF'].idxmin()]
            Data2 = pd.read_csv(outfile2, engine='python')
            subset2 = Data2.loc[Data2['Inv_RF'].idxmin()]
            
            if subset1["Inv_RF"] < subset2["Inv_RF"]:
                pd.Series.to_csv(subset1,cwd+"Parse_Results/Governing/"+truckNames[j]+"_"+"Governing_Rating"+ ".txt")
            else:
                pd.Series.to_csv(subset2,cwd+"Parse_Results/Governing/"+truckNames[j]+"_"+"Governing_Rating"+ ".txt")
            
            partialDrop = (Data1["Inv_LimitState"] == "Partial Horz. Shear") | (Data1["Inv_LimitState"] == "Partial Vert. Shear")
            partialIndices = [int(i) for i in Data1.loc[partialDrop].index]
            Data1 = Data1.drop(partialIndices)
            subset11 = Data1.loc[Data1['Inv_RF'].idxmin()]
        
            if subset11["Inv_RF"] < subset2["Inv_RF"]:
                pd.Series.to_csv(subset11,cwd+"Parse_Results/Governing/No_PS/"+truckNames[j]+"_"+"Governing_Rating_No_PS"+ ".txt")
        
            else:
                pd.Series.to_csv(subset2,cwd+"Parse_Results/Governing/No_PS/"+truckNames[j]+"_"+"Governing_Rating_No_PS"+ ".txt") 
            
            
        else:    
            fn = open(outfile1,"w")
            
            for i in range(len(rating_rows_1[j])):
                if i == 0:
                    fn.write("Panel_Point"+","+ "Truss_Member"+","+ "Legal_Op_LimitState"+","+ "Legal_Op_RF"+"\n")
                    fn.write(rating_rows_1[j][i][0]+","+ rating_rows_1[j][i][1]+","+  rating_rows_1[j][i][2]+","+ rating_rows_1[j][i][3]+"\n")
                    
                else:
                    fn.write(rating_rows_1[j][i][0]+","+ rating_rows_1[j][i][1]+","+  rating_rows_1[j][i][2]+","+ rating_rows_1[j][i][3]+"\n")
            
            fn.close()
            
            fn2 = open(outfile2,"w")
            
            for i in range(len(rating_rows_2[j])):
                if i == 0:
                    fn2.write("Panel_Point"+","+  "Legal_Op_LimitState"+","+  "Legal_Op_RF"+"\n")
                    fn2.write(rating_rows_2[j][i][0]+","+  rating_rows_2[j][i][1]+","+ rating_rows_2[j][i][2]+"\n")
                    
                else:
                    fn2.write(rating_rows_2[j][i][0]+","+  rating_rows_2[j][i][1]+","+ rating_rows_2[j][i][2]+"\n")
            
            fn2.close()
        
            Data1 = pd.read_csv(outfile1, engine='python')
            subset1 = Data1.loc[Data1['Legal_Op_RF'].idxmin()]
            Data2 = pd.read_csv(outfile2, engine='python')
            subset2 = Data2.loc[Data2['Legal_Op_RF'].idxmin()]
            
            if subset1["Legal_Op_RF"] < subset2["Legal_Op_RF"]:
                pd.Series.to_csv(subset1,cwd+"Parse_Results/Governing/"+truckNames[j]+"_"+"Governing_Rating"+ ".txt")
            else:
                pd.Series.to_csv(subset2,cwd+"Parse_Results/Governing/"+truckNames[j]+"_"+"Governing_Rating"+ ".txt")
            
            partialDrop = (Data1["Legal_Op_LimitState"] == "Partial Horz. Shear") | (Data1["Legal_Op_LimitState"] == "Partial Vert. Shear")
            partialIndices = [int(i) for i in Data1.loc[partialDrop].index]
            Data1 = Data1.drop(partialIndices)
            subset11 = Data1.loc[Data1['Legal_Op_RF'].idxmin()]
        
            if subset11["Legal_Op_RF"] < subset2["Legal_Op_RF"]:
                pd.Series.to_csv(subset11,cwd+"Parse_Results/Governing/No_PS/"+truckNames[j]+"_"+"Governing_Rating_No_PS"+ ".txt")
        
            else:
                pd.Series.to_csv(subset2,cwd+"Parse_Results/Governing/No_PS/"+truckNames[j]+"_"+"Governing_Rating_No_PS"+ ".txt") 
        
# put the governing file higher up so it won't get destroyed           
    for i in ["Governing/"]:
        cwd3 = cwd+"Parse_Results/"+i
        results = [f for f in os.listdir(cwd3) if os.path.isfile(cwd3+f)]
        result_names = [k.replace(".txt","") for k in results]
        outfile3 = cwd+"All_Results_"+differentiator+".txt"
        for j in range(len(results)):
            Data = pd.read_csv(cwd3+results[j], engine='python')
            Data["Truck"]=result_names[j]
            pd.DataFrame.to_csv(Data,outfile3, mode = 'a', index=False, line_terminator = "\n")
            Data.columns = [0,1,2]
            if "Left" in truss:
                if "EV" not in result_names[j]:
                    
                    a = Data.loc[Data[0] == 'Inv_RF']
                    left.append((a[1].values[0], a[2].values[0]))
                else:
                    a = Data.loc[Data[0] == 'Legal_Op_RF']
                    left.append((a[1].values[0], a[2].values[0]))
            else:
                if "EV" not in result_names[j]:
                    a = Data.loc[Data[0] == 'Inv_RF']
                    right.append((a[1].values[0], a[2].values[0]))
                else:
                    a = Data.loc[Data[0] == 'Legal_Op_RF']
                    right.append((a[1].values[0], a[2].values[0]))
                
                
                
                
                
                


    if "Right" in truss:
        governings = {}
        governings2 = {}
        for i in range(len(left)):
            if float(left[i][0])<float(right[i][0]):
                governings[left[i][1]]="LeftTruss"
                governings2[left[i][1]]="LeftTruss"
            elif float(left[i][0])==float(right[i][0]):
                governings[left[i][1]]="LeftTruss"
                governings2[left[i][1]]="Both"
            else:
                governings[right[i][1]]="RightTruss"
                governings2[right[i][1]]="RightTruss"
                
        cwd3 =  cwd+"Parse_Results/Governing/"   
        results = [f for f in os.listdir(cwd3) if os.path.isfile(cwd3+f) and "All_Results" not in f]
        result_names = [k.replace(".txt","") for k in results]
        outfile4 = Fwd+"Overall_Results_"+differentiator+".txt"
        for j in range(len(results)):
            gov_cwd = r'C:\Users\uname\Documents\AASHTOWARE\BrDR70\BIN\Span\Truss\Method'.replace("\\","/").replace("BIN",BIN).replace("Truss",governings[result_names[j]]).replace("Span",Span).replace("Method",Method).replace("uname",uname) + "/" 
            gov_cwd += "Parse_Results/Governing/" 
            Data = pd.read_csv(gov_cwd+results[j], engine='python')
            Data["Truck"]=result_names[j]
            pd.DataFrame.to_csv(Data,outfile4, mode = 'a', index=False, line_terminator = "\n")    
            
            
            
            
            
            
        
                
        

 

