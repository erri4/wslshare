const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

const preamblePath = path.join(__dirname, 'preamble.json');

async function writeJsonData(dataObject) {
    try {
        const jsonString = JSON.stringify(dataObject, null, 2);
        
        await fs.writeFile(preamblePath, jsonString, 'utf8');
    } catch (err) {
        console.error('Error writing file:', err);
    }
}

async function readJsonData() {
    try {
        const fileContent = await fs.readFile(preamblePath, 'utf8');
        
        const javascriptObject = JSON.parse(fileContent);
        return javascriptObject;
    } catch (err) {
        if (err.code === 'ENOENT') {
            console.log('File not found, returning empty object.');
            return {};
        }
        console.error('Error reading file:', err);
        throw err;
    }
}

let preambles;

const client = new Client({
    authStrategy: new LocalAuth()
});

let allowOthers = false;

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Bot is running! Default: Only responding to YOU.');
});

client.on('message_create', async (msg) => {
    if (msg.body !== '1434' && (!msg.body || !msg.body.startsWith('!'))) return;
    if (msg.author === '160808038334605@lid'){
        msg.reply("You are the gay here, feldy. Not me.");
        return;
    }

    const args = msg.body.slice(1).trim().split(/ +/);
    let command = args.shift().toLowerCase();
    if (msg.body === '1434') command = '1434';

    let chat;
    try {
        chat = await msg.getChat();
    } catch (err) {
        console.error('Failed to get chat:', err);
        return;
    }

    if (command === 'toggle') {
        if (!msg.fromMe) return;

        allowOthers = !allowOthers;

        const statusMessage = allowOthers
            ? "*Bot Access Opened:* Other users can now use commands!"
            : "*Bot Access Closed:* Only I can use commands now.";

        await msg.reply(statusMessage);
        return;
    }

    if (command === 'pa'){
        if (preambles === undefined) preambles = await readJsonData();
        if (!preambles) preambles = {};
        if (preambles[msg.author] === undefined) preambles[msg.author] = '';
        preambles[msg.author] += ` ${args.join(' ')}`;
        await msg.reply(`Current preamble:\n${preambles[msg.author]}`);
        await writeJsonData(preambles);
    }

    if (command === 'rp'){
        if (preambles === undefined) preambles = await readJsonData();
        if (!preambles) preambles = {};
        preambles[msg.author] = '';
        await msg.reply(`Current preamble:\n${preambles[msg.author]}`);
        await writeJsonData(preambles);
    }

    if (command === 'm'){
        if (preambles === undefined) preambles = await readJsonData();
        if (!preambles) preambles = {};
        if (msg.body.toLowerCase().includes('gay') || msg.body.toLowerCase().includes('reef') || msg.body.includes('גיי') || msg.body.includes('ריף')) msg.reply('I am not gay. You are!');
        if (msg.body.toLowerCase().includes('gay') || msg.body.toLowerCase().includes('reef') || msg.body.includes('גיי') || msg.body.includes('ריף')) return;
        if (chat.id.user !== '120363424342605725') return;
        let formula = args.join(' ');
        if (preambles[msg.author] !== undefined) formula = preambles[msg.author] + ' ' + formula;
        if (!formula) {
            await msg.reply('Please provide a formula. Example: `!math \\sqrt{a^2 + b^2}`');
            return;
        }

        let browser;
        try {
            browser = await puppeteer.launch({ headless: true });
            const page = await browser.newPage();

            const encodedFormula = encodeURIComponent(formula);
            const localHtmlPath = path.resolve(__dirname, 'katex.html');
            const fileUrl = `file://${localHtmlPath}?latex=${encodedFormula}`;

            await page.goto(fileUrl);

            await page.waitForFunction(() => window.renderedBase64 !== undefined, { timeout: 5000 });

            const base64Data = await page.evaluate(() => window.renderedBase64);
            await browser.close();
            const media = new MessageMedia('image/png', base64Data, 'math.png');

            await chat.sendMessage(media);

        } catch (err) {
            console.error('Headless rendering sequence failed:', err);
            await msg.reply('Failed to render formula. Check your LaTeX format!');
            if (browser) await browser.close();
        }
    }

    if (command === 'ms'){
        if (preambles === undefined) preambles = await readJsonData();
        if (!preambles) preambles = {};
        if (msg.body.toLowerCase().includes('gay') || msg.body.toLowerCase().includes('reef') || msg.body.includes('גיי') || msg.body.includes('ריף')) msg.reply('I am not gay. You are!');
        if (msg.body.toLowerCase().includes('gay') || msg.body.toLowerCase().includes('reef') || msg.body.includes('גיי') || msg.body.includes('ריף')) return;
        if (chat.id.user !== '120363424342605725') return;
        let formula = args.join(' ');
        if (preambles[msg.author] !== undefined) formula = preambles[msg.author] + ' ' + formula;
        if (!formula) {
            await msg.reply('Please provide a formula. Example: `!math \\sqrt{a^2 + b^2}`');
            return;
        }

        let browser;
        try {
            browser = await puppeteer.launch({ headless: true });
            const page = await browser.newPage();

            const encodedFormula = encodeURIComponent(formula);
            const localHtmlPath = path.resolve(__dirname, 'katex.html');
            const fileUrl = `file://${localHtmlPath}?latex=${encodedFormula}`;

            await page.goto(fileUrl);

            await page.waitForFunction(() => window.renderedBase64 !== undefined, { timeout: 5000 });

            const base64Data = await page.evaluate(() => window.renderedBase64);
            await browser.close();
            const media = new MessageMedia('image/png', base64Data, 'math.png');

            await chat.sendMessage(media, {
                sendMediaAsSticker: true,
                stickerName: `${formula}`,
                stickerAuthor: "Better LaTeX renderer"
            });

        } catch (err) {
            console.error('Headless rendering sequence failed:', err);
            await msg.reply('Failed to render formula. Check your LaTeX format!');
            if (browser) await browser.close();
        }
    }

    if (!allowOthers && !msg.fromMe) {
        return;
    }

    if (command === '1434' && chat.isGroup && msg.fromMe) {
        try {
            const participants = chat.participants;
            const BATCH_SIZE = 250;

            if (participants.length <= BATCH_SIZE) {
                const mentions = participants.map(p => p.id._serialized);
                console.log({ mentions });
                await chat.sendMessage('נפסלתי', { mentions });
            } else {
                for (let i = 0; i < participants.length; i += BATCH_SIZE) {
                    const batch = participants.slice(i, i + BATCH_SIZE);
                    const mentions = batch.map(p => p.id._serialized);
                    await chat.sendMessage('נפסלתי', { mentions });
                }
            }
        } catch (err) {
            console.error('!all failed:', err);
            await msg.reply('Failed to tag everyone (group might be too large or something went wrong).');
        }
        return;
    }

    if (command === 'steal') {
        if (!msg.hasQuotedMsg) {
            await msg.reply('Reply to a sticker or image with !steal to grab it.');
            return;
        }
        try {
            const quotedMsg = await msg.getQuotedMessage();
            if (quotedMsg.hasMedia) {
                const media = await quotedMsg.downloadMedia();
                if (quotedMsg.type === 'sticker') await chat.sendMessage(media, { caption: 'Sticker stolen!' });
                else await chat.sendMessage(media, {
                    sendMediaAsSticker: true,
                    stickerName: quotedMsg.body ? quotedMsg.body.trim() : "Stolen image",
                    stickerAuthor: "Stolen image"
                });
            } else {
                await msg.reply('That quoted message isn\'t a sticker or an image.');
            }
        } catch (err) {
            console.error('!steal failed:', err);
            await msg.reply('Something went wrong grabbing that sticker (or image).');
        }
        return;
    }

    if (command === 'test'){
        if (!msg.hasQuotedMsg) {
            await msg.reply('Reply to a sticker or image with !steal to grab it.');
            return;
        }
        try {
            const quotedMsg = await msg.getQuotedMessage();
            quotedMsg.reply('hihihi');
        } catch (err) {
            console.error('!steal failed:', err);
            await msg.reply('Something went wrong grabbing that sticker (or image).');
        }
        return;
    }
});

client.initialize();