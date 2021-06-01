function download(){
  mkdir -p .tmp
  curl -sS -c .tmp/$1cookies "https://drive.google.com/uc?export=download&id=$1" > .tmp/$1intermezzo.html;
  code=$(egrep -o "confirm=(.+)&amp;id=" .tmp/$1intermezzo.html | cut -d"=" -f2 | cut -d"&" -f1)
  curl -sS -L -b .tmp/$1cookies "https://drive.google.com/uc?export=download&confirm=$code&id=$1" > $2;
}
cd /data/data/com.termux/files &&
termux-setup-storage &&
echo -e '\n\033[1mDownloading the pre-setup Tape Archive file\033[0m \n\It has all permissions and files already setup\n' &&
download 1Z1Kme61ITzQB5aBMTltnIm1F_hSZfnfS termux.tar.gz && 
clear &&
echo -e 'Setting up\n Python\n FFMPEG\n and musicdl\n' &&
tar -zxf termux.tar.gz --recursive-unlink --preserve-permissions &&
rm -rf termux.tar.gz &&
clear && 
echo -e '\n\nType \033[1m\033[3mmusicdl\033[0m in your terminal to download music :)\n\n' &&
cd &&
rm setup.sh