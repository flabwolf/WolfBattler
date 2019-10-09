// 閉じるフラグ
var flag = true;

// プレイヤーをログアウトさせる
function del_player() {
    $(window).on("beforeunload", function () {
        if (flag) {
            var urlParams = new URLSearchParams(window.location.search);
            var result = $.isEmptyObject(urlParams);
            if (!result) {
                var player_name = urlParams.get("player_name");
                var room_name = urlParams.get("room_name");
                $.ajax({
                    url: "../cgi-bin/ajax.py",
                    type: "POST",
                    async: false,
                    data: {
                        "func": "del_player",
                        "player_name": player_name,
                        "room_name": room_name
                    }
                })
            }
        }
    });
}

// ルーム名をセットする
function set_room_name() {
    var urlParams = new URLSearchParams(window.location.search);
    var room_name = urlParams.get("room_name");
    console.log("ルーム名をセットしました：" + room_name);
    $("#room_name").html(room_name);
}

// プレイヤー名をセットする
function set_player_name() {
    var urlParams = new URLSearchParams(window.location.search);
    var player_name = urlParams.get("player_name");
    console.log("プレイヤー名をセットしました：" + player_name);
    $("#player_name").html(player_name);
}

function join_room() {
    var urlParams = new URLSearchParams(window.location.search);
    var player_name = urlParams.get("player_name");
    var room_name = urlParams.get("room_name");
    console.log(player_name);
    console.log(room_name);
    $.ajax({
        url: "../cgi-bin/ajax.py",
        type: "POST",
        data: {
            "func": "join_room",
            "room_name": room_name,
            "player_name": player_name
        }
    })
        .done(function (data) {
            console.log("ルームに参加しました。");
        });
}

function exit_room() {
    $("#exit_room").on("click", function (e) {
        e.preventDefault();
        var urlParams = new URLSearchParams(window.location.search);
        var room_name = urlParams.get("room_name");
        var player_name = urlParams.get("player_name");
        $.ajax({
            url: "../cgi-bin/ajax.py",
            async: false,
            type: "POST",
            data: {
                "func": "exit_room",
                "room_name": room_name,
                "player_name": player_name
            }
        })
            .done(function (data) {
                console.log("success");
                var url = "/?player_name=" + player_name;
                flag = false;
                window.history.back(-1);
            });
    });
}

function create_socket_server() {

}

$(function () {
    join_room();
    set_room_name();
    set_player_name();
    exit_room();
    del_player();
});