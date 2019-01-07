# metaPy

## Using Python and a Raspberry Pi to Update Icecast Audio Feeds with Scanner Alpha Tags

These python scripts will add the ability to update Icecast feed metadata via a Raspberry Pi or other network connected computer with a serial connection.  They are compatible with the following Uniden Scanners:

* BCT8
* BCT15
* BCT15X
* BCD996T
* BCD996XT
* BC346T
* BC346XT
* BCD396T
* BCD396XT
* BC898T

Functionality could be added for other Uniden scanners such as the 780XLT, 785D, 796D, and 898T, but as of now I don’t have access to any of these models for testing.

To implement the script, download the script by right clicking on the appropriate link below and click “Save As”.  You can do this from the Raspberry Pi or from another computer and use any number of tools such as ssh and scp to copy the file to your desired location on your Raspberry Pi.

Modify the configuration section as necessary.

To connect your scanner you’ll need a USB to serial adapter. If it’s the first one connected, it should show up as `/dev/ttyUSB0`. You can check and see by going to /dev and list the files and look for `ttyUSB0` or something similar.  Also make sure that the baudrate in the script is the same as the baudrate set in your scanner.
The script uses two Python modules requests and serial that may or may not be installed on your Raspberry Pi. You can install these packages by using apt-get:
`sudo apt-get install python-serial, python-requests`
 

To run the script, change directories to the location the script is saved. Then type python metaPy.py to begin the script. If it is running, you will see it print out talkgroup information, time information and an update status:

`Davis County Sim 11232 Syracuse PD 2 C`

`Thu Jun 13 21:07:03 2013`

`Icecast Update OK`

`Davis County Sim 10688 Davis Ops 2`

`Thu Jun 13 21:07:21 2013`

`Icecast Update OK`

The script can be placed in the background by typing ctrl-z and then bg. It can be brought back to the foreground by typing fg.You can also start the script detached from the console by adding an & to the end of the command: python metaPy.py &  .

To stop the script, simply type `ctrl-c`, or find the process and kill it.

BCT8/BCT898 Tagging

The BCT8/BCT898 scanners don’t support frequency tagging. This can be
implemented however, by creating a CSV file with frequencies in the first column
and Alpha Tags in the second column.  Place this file in the same directory
as the MetaPy8.py script. In the script USER CONFIGURATION section set the
variable csvFile to the name of the .csv file you created with your
frequency/tag data. When the script is run it will lookup data in the file and
if a tag is found for the frequency, it will add that to the feed metadata.

Note: Each time you make changes to the lookup table, you need to restart the
metaPy8.py script.  The frequency should be in the format: `XXX.XXXX`. If
there are only 2 digits before the decimal point, add a space character to the
frequency area of the table:

`132.6500,KSLC Tower`

`47.5125,CHP`

By using Darkice to feed the audio and this metaPy.py script to feed the alpha tags, you now have a 5W streaming media box to stream both scanner audio and text alpha tags.
