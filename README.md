# wpp
This is for automate my wallpaper with images obtained from GOES16 at current time.(but 15 or 45 min later, this time were spent in verifying the picture)

Now this repository will be used for teaching friends to programing in python.

In ubuntu 22.04 we can automate with:


1 - Copy the wpp.py to some folder

2 - To set the correct path : open the wallpaper folder and copy the name of your currently wallpaper

	path_to_current_wpp = 'Pictures/Wallpapers/your-current-wallpaper-file-name.jpg'
	(in general case is)
	path_to_current_wpp = 'Pictures/Wallpapers/wallpaper.jpg'

2 - In ubuntu terminal:  $ whereis python

3 - $ crontab -e

4 - Add this line at the end:
	
	0,15,30,45 * * * * (some python obtained with (2) whereis command) path_to_file/wpp.py

5 - to save hit : ctrl+o 
6 - to exit hit : ctrl+x

- mine case example:
0,15,30,45 * * * * /home/v/anaconda3/bin/python Desktop/wpp.py



