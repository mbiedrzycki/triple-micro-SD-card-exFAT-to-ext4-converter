#! /usr/bin/python

import tkinter
from tkinter import messagebox
from tkinter import ttk
import os
import subprocess

def convert():
	devices = ("/dev/sdc","/dev/sdd","/dev/sde","/dev/sdf","/dev/sdg","/dev/sdh","/dev/sdi","/dev/sdj","/dev/sdk","/dev/sdl","/dev/sdm","/dev/sdn","/dev/sdo","/dev/sdp","/dev/sdr","/dev/sds")
	for x in devices:
		umount = ("sudo -s umount "+x)
		umountPartition = ("sudo -s umount "+x +"1")
		mount = ("sudo -s mount "+x+" /media/flasher")
		wipefs = ("sudo -s wipefs -a -f "+x)
		mkfs = ("sudo -s mkfs -t ext4 "+x)
		mkfs1 = ("sudo -s mkfs -t ext4 "+x+"1")
		mountPathX = ("sudo -s df -h "+x)
		condition=("sudo -s fdisk -l "+x)
		sgdisk = ("sgdisk -n 0:0:0 " + x)
		conditionExt4 = ("df -T " +x)
		os.system(umount)
		diskUsage = subprocess.getoutput(condition)
		diskUsage = diskUsage.split(sep=None, maxsplit =-1) #output to list
		diskUsage = diskUsage[2] #getting size from list
		diskUsage = diskUsage[:-2] #deleting GB letter to change variable type to int
		if diskUsage == "moż": #if cannot disk read
			print("Nie wykryto "+str(x))
		else:
			diskUsage = float(diskUsage)
			diskUsage = math.floor(diskUsage)
			print("Pojemność karty ",x,":",diskUsage, "GB")
			if diskUsage!=232:
				print("Niepowodzenie, HDD, SSD lub inne usb.")
			else:	
				os.system(umount)
				os.system(umountPartition)
				os.system(wipefs)
				os.system(mkfs)
				os.system(mount)
				path = subprocess.getoutput(mountPathX)
				path = path.split(sep=None, maxsplit =-1) #output to list
				mountPath = path[13]
				permission= ("sudo -s chmod 777 "+ mountPath)
				os.system(permission)
				os.system(mount)
				partitionType=subprocess.getoutput(conditionExt4)
				partitionType=partitionType.split(sep=None, maxsplit =-1)
				partitionType = partitionType[10]
				partitionTypeInfo= ("Udało się. Format karty "+ str(x)+": " + str(partitionType))
				if partitionType == "ext4":
					if x not in ext4DevicesList:
						os.system(umount)
						ext4DevicesList.append(x)
				else:
					messagebox.showerror("Niepowodzenie", "Błąd! Zły format karty!")
					os.system(umount)
				os.system(sgdisk)
				os.system(mkfs1)
	if len(ext4DevicesList) == 3:
		messagebox.showinfo("Informacja", "Sformatowano " + str(len(ext4DevicesList)) + " karty. " + "\n" + str(ext4DevicesList[0]) + "\n"+ str(ext4DevicesList[1])  +"\n"+ str(ext4DevicesList[2]))
	elif len(ext4DevicesList) == 2:
		messagebox.showinfo("Informacja", "Sformatowano " + str(len(ext4DevicesList)) + " karty. " + "\n" + str(ext4DevicesList[0]) + "\n"+ str(ext4DevicesList[1]))
	elif len(ext4DevicesList) == 1:
		messagebox.showinfo("Informacja", "Sformatowano " + str(len(ext4DevicesList)) + " karty. " + "\n" + str(ext4DevicesList[0]))	
	elif len(ext4DevicesList) > 3: 
		messagebox.showerror("Błąd krytyczny!", "Zawołaj pomoc!")
	else:
		messagebox.showerror("Niepowodzenie", "Nie sformatowano żadnej karty!")

def diskInfo():
	list =[]
	newWindow = tkinter.Toplevel(top)
	top.eval(f'tk::PlaceWindow {str(newWindow)} center')
	newWindow.geometry("620x270")
	description = tkinter.Label(newWindow, text ="ODCZYT DYSKÓW")
	description.config(font = ("Cagliari", 14))
	description.pack()
	if len(ext4DevicesList) ==0:
		messagebox.showinfo("Info", "Przed odczytem sformatuj karty!")
		newWindow.destroy()
	else:
		for i in ext4DevicesList:
			mount = ("sudo -s mount "+i+"1"+" /media/flasher")
			os.system(mount)
			disksInfoCommand=("df -T "+i+"1")
			disks=subprocess.getoutput(disksInfoCommand)
			list.append(disks)	
			disksInfoCommand2=("ls -l "+i+"*")
			disks2=subprocess.getoutput(disksInfoCommand2)
			list.append(disks2)
			umount = ("sudo -s umount "+i+"1")
			os.system(umount)
			listEnterLine = "\n".join(list)
			listEnterLine = "\n".join(list)
		lab = tkinter.Label(newWindow, text = listEnterLine ).pack()

def instruction():
	instructionWindow=tkinter.Toplevel(top)
	top.eval(f'tk::PlaceWindow {str(instructionWindow)} center')
	instructionWindow.geometry("920x670")
	instructionWindow.configure(bg="white")
	instructionText = "INSTRUKCJA" + '\n'+ '\n' + "1. Przed uruchomieniem programu upewnij się, że HUB z kartami SD jest podłączony do komputera."  +'\n' + "2. Jeśli diody pendrivów  świecą się na niebiesko kliknij START."+'\n' + "3. Po pomyślnej konwersji kart pojawi się dodatkowe okienko z informacją o ilości sformatowanych kart. "
	instructionText2 = "4. Jeśli widoczna ilość zgadza się z ilością kart włożonych do HUBa, kliknij ODCZYT DYSKÓW." + '\n' +"5. Na poniższym obrazku przedstawiony został poprawny odczyt." + '\n'+" Każda karta powinna mieć format ext4 oraz powinna zawierać dwie partycje(np. /dev/sdc i /dev/sdc1). "
	instructionText3 = "6. Jeśli poprzednie podpunkty się zgadzają, można wyjąć karty i włożyć nowe."
	instructionDescription = tkinter.Label(instructionWindow, text =instructionText)
	instructionDescription.config(font = ("Cagliari", 12))
	instructionDescription.configure(bg="white")
	instructionDescription.pack()
	img = tkinter.PhotoImage(file = "instruction1.png")
	labelImg = tkinter.Label(instructionWindow, image = img).pack()
	instructionDescription2 = tkinter.Label(instructionWindow, text =instructionText2)
	instructionDescription2.config(font = ("Cagliari", 12))
	instructionDescription2.configure(bg="white")
	instructionDescription2.pack()
	img2 = tkinter.PhotoImage(file = "instruction2.png")
	labelImg2 = tkinter.Label(instructionWindow, image = img2).pack()
	instructionDescription2 = tkinter.Label(instructionWindow, text =instructionText3)
	instructionDescription2.config(font = ("Cagliari", 12))
	instructionDescription2.configure(bg="white")
	instructionDescription2.pack()
	instructionWindow.mainloop()

	
top = tkinter.Tk()
top.eval('tk::PlaceWindow . center')
top.title("Karty SD - KEOLIS")
top.geometry("540x250")
ext4DevicesList = []
startInfo = "Konwertowanie kart MicroSD - TFT"+'\n'+"Przez rozpoczęciem zapoznaj się z instrukcją." 
description = tkinter.Label(top, text =startInfo)
description.config(font = ("Cagliari", 10))
description.pack()
disksButton = tkinter.Button(top, height =2, width = 20, text = "INSTRUKCJA", command = instruction).pack(pady=10)
startButton = tkinter.Button(top, height =2, width = 20, text = "START", command = convert).pack(pady=10)
disksButton = tkinter.Button(top, height =2, width = 20, text = "ODCZYT DYSKÓW", command = diskInfo).pack(pady=10)
top.mainloop()
