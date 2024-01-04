import { NFTStorage, Blob, File } from "nft.storage";
import { config } from "dotenv";
import { readFile } from "fs/promises";
import { createWriteStream } from 'fs';
import { format } from 'util';
var log_file = createWriteStream('debug.log', {flags : 'a'});
var log_stdout = process.stdout;

console.log = function(d) { //
  log_file.write(format(d) + '\n');
  log_stdout.write(format(d) + '\n');
};

config();

async function sleep(seconds) {
    return new Promise((resolve) => {
        setTimeout(resolve, seconds * 1000);
    });
}

async function getImage() {
    const image_path = process.argv[2];
    // console.log(data)
    const image = await readFile(image_path);
    return image;
}

async function upload(client, image) {

    let retry_count = 0;
    while (true) {
        try {
            const cid = await client.storeBlob(new Blob([image]));
            return cid;
        } catch (error) {
            if (error.message !== "Timed out waiting for pinning") {
                throw error;
            }

            if (retry_count > 9) {
                throw error;
            }

            // console.log(`retrying after 10 seconds, retry count: ${retry_count}`);
            await sleep(10);
            retry_count++;
        }
    }
}

async function main() {
    const api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGMwMGE2NmY3QzE1OWE4N0M0MWUwNEFlMDZlODNmOGE0Yjc1OWE0N0QiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY4MTMxNDgzNTA2NSwibmFtZSI6InVuc3BlbmQifQ.lOD_foG9DavtYnMfvxys9zWb-2TOUOe7cf6Su6c1J_s";
    const client = new NFTStorage({ token: api_key });
    const image = await getImage();

    const cid = await upload(client, image);
    console.log({ "cid": cid });
}


main().catch((error) => {
    console.error(error);
    process.exit(1);
});
