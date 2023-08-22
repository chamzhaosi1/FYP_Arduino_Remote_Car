    const puppeteer = require('puppeteer-core');

    function delay(time) {
        return new Promise(function(resolve) { 
            setTimeout(resolve, time)
        });
    }

    (async () => {
        const browser = await puppeteer.launch({executablePath: '/usr/bin/chromium-browser', 
            args: ['--use-fake-ui-for-media-stream', '--ignore-certificate-errors'], dumpio: true, ignoreHTTPSErrors: true, headless:true,}); // dumpio get all console log 

        const page = await browser.newPage();

        const mac_address = process.argv[2]
        const url = 'https://romo.kynoci.com:4200/login_romo/' + mac_address
        console.log(url)
        await page.goto(url, {
          waitUntil: 'networkidle0',
          timeout: 300000,
        });
        
        page
        .on('console', message =>{
          // console.log("console")
          console.log(`${message.type().substr(0, 3).toUpperCase()} ${message.text()}`)})
        .on('pageerror', ({ message }) => {
          // console.log("pageerror")
          console.log(message)
        })
        .on('response', response =>{
          // console.log("response")
          console.log(`${response.status()} ${response.url()}`)})
        .on('requestfailed', request =>{
          console.log(`${request.failure().errorText} ${request.url()}`)
          // console.log("requestfailed")
        })

        // await page.waitForSelector('input[name=userNameInput]');
        // await page.$eval('input[name=userNameInput]', el => el.value = '00:B0:D0:63:C2:26');
        // const loingBtn = await page.$('#loginButton');
        // loingBtn.click();
        // await delay(5000);

        // const answerBtn = await page.$('#answerButton');
        // answerBtn.click();
        // await delay(5000);

        await page.screenshot({path: 'screeshot12.png'});
        // await browser.close();
    })();
