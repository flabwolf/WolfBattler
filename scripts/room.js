// ルーム名をセットする
function set_room_name() {
    var urlParams = new URLSearchParams(window.location.search);
    var room_name = urlParams.get("room_name");
    console.log(room_name);
    $("#room_name").html(room_name);
    set_player_name(room_name);
}

// プレイヤー名をセットする
function set_player_name(room_name) {
    $.ajax({
        url: "../cgi-bin/ajax.py",
        dataType: "json",
        type: "POST",
        data: {
            "func": "get_player_name",
            "room_name": room_name
        }
    })
        .done(function (data) {
            console.log("success");
            console.log(data);
            $("#player_name").html(data["player_name"]);
        });
}

function create_socket_server() {

}

$(function () {
    set_room_name()
});