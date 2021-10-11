#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import winreg
import ctypes
from shutil import which




def check_vlc_path() -> bool:
    """
    Function to check if vlc is present in path
    """

    if which('vlc') is None:
        print('''[ERROR] :: vlc not added to system path
        
        Please add vlc in your environment variables and then restart the program.
        You can also add vlc to path, type:  yt --vlc <path-to-vlc>
        
        
        Read more: https://github.com/PaulSayantan/yt/blob/main/README.md
        For further assistance, please put an issue at: https://github.com/PaulSayantan/yt/issues/new''')
        return False
    else:
        print('[SUCCESS] :: vlc is present at path')
        return True




def add_vlc_path(program_path: str):
    """
    Function to add vlc program to the system path

    Args:
        program_path (str): path where vlc program is installed in the system
    
    """

    if os.name == "nt":  # Windows systems
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                existing_path_value = winreg.EnumValue(key, 3)[1]

                # Takes the current path value and appends the new program path
                new_path_value = existing_path_value + program_path + ";"

                # updating path
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)

                # Tell other processes to update their environment
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
            SendMessageTimeoutW(
                HWND_BROADCAST,
                WM_SETTINGCHANGE,
                0,
                "Environment",
                SMTO_ABORTIFHUNG,
                5000,
                ctypes.byref(result),
            )
    else:
        # if you are using any other shells like zsh or fish, please change .bashrc accordingly
        with open(f"{os.getenv('HOME')}/.bashrc", "a") as bash_file:
            bash_file.write(f'\nexport PATH="{program_path}:$PATH"\n')

        # update path
        os.system(f". {os.getenv('HOME')}/.bashrc")
    print(f"Added {program_path} to path, please restart shell for changes to take effect")




if __name__ == '__main__':
    check_vlc_path()
