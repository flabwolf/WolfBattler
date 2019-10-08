// 作成したルームに参加する
function join_room(room_name) {
    player_name = $("#player_name").text();
    console.log(player_name)
    console.log(room_name);
    $.ajax({
        url: "cgi-bin/ajax.py",
        type: "POST",
        data: {
            "func": "join_room",
            "room_name": room_name,
            "player_name": player_name
        }
    })
        .done(function (data) {
            console.log("success");
            window.location.href = "htmls/room.html";
        });
}

// ルームを生成する
function create_room() {
    $("#create_room").on("click", function (e) {
        // e.preventDefault();
        var room_name = $("[name='room_name']").val();
        console.log(room_name);
        $.ajax({
            url: "cgi-bin/ajax.py",
            type: "POST",
            dataType: "json",
            data: {
                "func": "create_room",
                "room_name": room_name
            }
        })
            .done(function (data) {
                console.log("success");
                console.log(data);
                join_room(data["room_name"]);

            })
            .fail(function (data) {
                console.log("fails");
                console.log(data);
            });
    });
}

// プレイヤーを生成する
function create_player() {
    $("#create_player").on("click", function (e) {
        e.preventDefault();
        var player_name = $("[name='player_name']").val();
        $.ajax({
            url: "cgi-bin/ajax.py",
            type: "POST",
            dataType: "json",
            data: {
                "func": "create_player",
                "player_name": player_name
            }
        })
            .done(function (data) {
                console.log("success");
                console.log(data)
                $("#player_name").html(data["player_name"])
            });
    });
}

$(function () {
    create_player();
    create_room();
});