const express = require('express');
const router = express.Router();
const path = require('path')
const { spawn } = require('child_process')
const { upload } = require('../middlewares');

function runScript(fileName) {
    return spawn('python', [
        "-u",
        path.join(__dirname, '/../detect/detectNode.py'),
        "--path", path.join(__dirname, `/../public/uploads/${fileName}`),
    ]);
}

router.post('/upload', upload.single('image'), (req, res, next) => {
    try {
        const subprocess = runScript(req.file.filename)
        subprocess.stdout.on('data', (data) => {
            const url = req.protocol + "://" + req.get("host");
            const outFile = url + "/" + data;
            return res.status(200).send(outFile);
        });
        subprocess.stderr.on('data', (data) => {
            console.log(`error:${data}`);
            next()
        });
        subprocess.stderr.on('close', () => {
            console.log("Done");
        });
    } catch (error) {
        next(error)
    }

})

module.exports = router