source ~/virtualenv/bin/activate
pip install selenium
pip list

cd ~

# curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y update
apt-get -y dist-upgrade
apt-get -y install unzip
apt-get -y install google-chrome-stable
apt-cache policy google-chrome-stable

chromium-browser --version
# wget https://chromedriver.storage.googleapis.com/95.0.4638.69/chromedriver_linux64.zip
# wget https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
rm -rf chromedriver_linux64.zip

# chromium-browser --new-window https://google.com

###############################################################################
### Step 2.B. : Manually Run Full Screen Browser only (a.k.a. Kiosk)
###############################################################################
# REFER : https://peter.sh/experiments/chromium-command-line-switches/
apt -y install psmisc
killall chromium
su - engineer -c 'DISPLAY=:0 chromium-browser \
    --no-first-run \
    --disable \
    --disable-translate \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --start-maximized \
    --incognito \
    --autoplay-policy=no-user-gesture-required \
    --use-fake-ui-for-media-stream \
    --kiosk "https://google.com" &'
    # --kiosk "https://vchat.kynoci.com" &'
    # --kiosk "https://vchat.kynoci.com/?name=r2&mac=ma:mr:33:89:23:01:f3:02" &'
    # --kiosk "https://meet.google.com/csx-exuq-dbk" &'


###############################################################################
### Step 1. : Headless chromium in raspberry pi
###############################################################################
# REFER: https://www.youtube.com/watch?v=6LnJ1zW5464
# REFER: https://www.npmjs.com/package/puppeteer-core
# REFER: https://stackoverflow.com/questions/48264537/auto-allow-webcam-access-using-puppeteer-for-node-js
# AS USER setup
apt-get -y install chromium-browser
apt-get -y install chromium-codecs-ffmpeg
apt-get -y install npm
# npm install puppeteer-core@v1.11.0
cd /home/engineer/romo_v2/chromium-browser
npm install puppeteer-core@v19.7.5
npm i puppeteer
cat > /home/engineer/romo_v2/chromium-browser/index.js << EOF
    const puppeteer = require('puppeteer-core');

    function delay(time) {
        return new Promise(function(resolve) { 
            setTimeout(resolve, time)
        });
    }

    (async () => {
        const browser = await puppeteer.launch({executablePath: '/usr/bin/chromium-browser', 
            args: ['--use-fake-ui-for-media-stream'], dumpio: true}); // dumpio get all console log 

        const page = await browser.newPage();
        const mac_address = process.argv[2]
        const url = 'https://romo.kynoci.com:4200/login_romo/' + mac_address
        await page.goto(url);

        // await page.waitForSelector('input[name=userNameInput]');
        // await page.\$eval('input[name=userNameInput]', el => el.value = '00:B0:D0:63:C2:26');
        // const loingBtn = await page.\$('#loginButton');
        // loingBtn.click();
        // await delay(5000);

        // const answerBtn = await page.\$('#answerButton');
        // answerBtn.click();
        // await delay(5000);

        await page.screenshot({path: 'screeshot12.png'});
        // await browser.close();
    })();
EOF
cat /home/engineer/romo_v2/chromium-browser/index.js
ls
node /home/engineer/romo_v2/chromium-browser/index.js e4:5f:01:42:52:3e


cat > /home/engineer/romo_v2/chromium-browser/index.js << EOF
    const puppeteer = require('puppeteer-core');

    function delay(time) {
        return new Promise(function(resolve) { 
            setTimeout(resolve, time)
        });
    }

    (async () => {
        const browser = await puppeteer.launch({executablePath: '/usr/bin/chromium-browser', 
            ignoreDefaultArgs: ['--mute-audio'],
            args: ['--use-fake-ui-for-media-stream', '--autoplay-policy=no-user-gesture-required', '--alsa-output-device=plug:hw']});
        const page = await browser.newPage();
        await page.goto('https://www.youtube.com/watch?v=o0j8UAKOPpY?autoplay=1');
        await page.screenshot({path: 'screeshot1.png'});
        await delay(5000);

        await page.screenshot({path: 'screeshot2.png'});
        // await browser.close();
    })();
EOF

