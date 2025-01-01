window.setInterval(
    function(){
        liveStream = document.getElementById("items").textContent.split(":");
        if (liveStream.at(-1).includes("https://roblox.com/")) {
            index = 0;
            temp = liveStream.at(-1).split(" ");
            while (index < temp.length) {
                if (temp[index].replace("Propst", " ").includes("https://roblox.com/")) {
                    window.open(temp[index].replace("Propst", " "));
                    console.log("Opened URL: "+temp[index]);
                    index = temp.length;
                }
                index++;
            }
        }
        console.log(liveStream.at(-1).split("AM")[1]);
    },
    100
)