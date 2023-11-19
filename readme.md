Very sloppy Readme for now

if you want to translate Teamchat you have to modify your language file
you can find this File here: 
C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\resource

in my Case i used csgo_english.txt

then you have to modify these Entries:

        "Game_radio"                        " %s1: %s2"
        "Game_radio_location"               " %s1﹫%s2: %s3"
        "Cstrike_Chat_CT_Loc"               " %s1﹫%s3: %s2"
        "Cstrike_Chat_T_Loc"                " %s1﹫%s3: %s2"
        "Cstrike_Chat_CT_Dead"              " %s1 [DEAD]: %s2"
        "Cstrike_Chat_T_Dead"               " %s1 [DEAD]: %s2"
        "Cstrike_Chat_CT"                   " %s1: %s2"
        "Cstrike_Chat_T"                    " %s1: %s2"
        "Cstrike_Chat_All"                  " [ALL] %s1: %s2"
        "Cstrike_Chat_AllDead"              " [ALL] %s1 [DEAD]: %s2"

and turn them into this:

        "Game_radio"                        " %s1: %s2"
        "Game_radio_location"               " %s1﹫%s2: %s3"
        "Cstrike_Chat_CT_Loc"               " [TEAM] %s1﹫%s3: %s2"
        "Cstrike_Chat_T_Loc"                " [TEAM] %s1﹫%s3: %s2"
        "Cstrike_Chat_CT_Dead"              " [TEAM] %s1 [DEAD]: %s2"
        "Cstrike_Chat_T_Dead"               " [TEAM] %s1 [DEAD]: %s2"
        "Cstrike_Chat_CT"                   " [TEAM] %s1: %s2"
        "Cstrike_Chat_T"                    " [TEAM] %s1: %s2"
        "Cstrike_Chat_All"                  " [ALL] %s1: %s2"
        "Cstrike_Chat_AllDead"              " [ALL] %s1 [DEAD]: %s2"

now all your TEAM Chat has a [TEAM] ind front of the Message and Allchat has [ALL] 


Example:  

![image](https://github.com/MeckeDev/cs2_translator/assets/43956685/71077f09-7bcb-49c8-875a-4e52b6929f11)

![image](https://github.com/MeckeDev/cs2_translator/assets/43956685/08f68b7e-c494-4c25-879b-c372dad49293)

