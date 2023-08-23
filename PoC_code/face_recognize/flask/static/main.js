$(document).ready(function () {
    $(document).ajaxStop(myInterval = setInterval(function() {
        $.ajax({
            url: "/unknown_face_detect",
            method: `GET`,
            error: (error) => {},
            success: (Response) => {
                console.log(typeof(Response))
                console.log(Response)

                if(Response === "true" || Response === "false"){

                    if (Response === "true"){
                        document.getElementById("snapshotBtn").disabled = false;
                        snapshotBtn = document.getElementById("snapshotBtn").classList;
                        snapshotBtn.add("btn-primary");
                        snapshotBtn.remove("btn-secondary");
                    }else{
                        document.getElementById("snapshotBtn").disabled = true;
                        snapshotBtn = document.getElementById("snapshotBtn").classList;
                        snapshotBtn.add("btn-secondary");
                        snapshotBtn.remove("btn-primary");
                    }
                }else{
                    // print(Response.redirect)
                    document.body.innerHTML = Response
                    clearInterval(myInterval);
                }
                    
            }
        })
    }, 800))
})

$(document).ready(function () {
    $("#snapshotBtn").on('click', function(){
        inputNewName = $(inputNewName).val()
        console.log(inputNewName)
        $.ajax({
            url: "/snapshot_unknown_face_detect",
            method: `POST`,
            data: {"inputNewName" : inputNewName},
            error: (error) => {},
            success: (Response) => {
                console.log(Response)
            }
        })
    })
})