'use strict';

function checkPLCStatus() {
  fetch('/weld/ping_plc/') // PLC에 ping 요청을 보내는 URL
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json(); // JSON 응답 처리
    })
    .then((data) => {
      const plcComElement = document.getElementById('plc_com');
      plcComElement.innerText = data.status; // 통신 상태 업데이트
    })
    .catch((error) => {
      console.error('Error checking PLC status:', error);
      document.getElementById('plc_com').innerText = '통신 비정상'; // 오류 발생 시 상태 업데이트
    });
}

// 현재 시간을 YY:DD:MM HH:mm:ss 형식으로 업데이트
// function updateCurrentTime() {
//   const now = new Date();
//   const year = now.getFullYear().toString(); // YY
//   const month = String(now.getMonth() + 1).padStart(2, '0'); // MM
//   const day = String(now.getDate()).padStart(2, '0'); // DD
//   const hours = String(now.getHours()).padStart(2, '0'); // HH
//   const minutes = String(now.getMinutes()).padStart(2, '0'); // mm
//   const seconds = String(now.getSeconds()).padStart(2, '0'); // ss

//   document.querySelector(
//     '#now_time'
//   ).innerText = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
// }
function updateTime() {
  const now = new Date();
  const formattedTime = now.toLocaleTimeString();
  const formattedDate = now.toLocaleDateString();
  document.getElementById(
    'now_time'
  ).innerText = `${formattedDate} ${formattedTime}`;
}

// 1초마다 주기적으로 데이터 갱신
setInterval(() => {
  checkPLCStatus();
  // updateCurrentTime();
  updateTime();
}, 1000);

// function updateData() {
//   fetch('/weld/latest_data/')
//     .then((response) => response.json())
//     .then((data) => {
//       // 최신 모델 정보 업데이트 document.getElementById('model_num').innerText =
//       data.latest_raw_data.model_id;
//       document.getElementById('model_name').innerText =
//         data.latest_raw_data.model_name;
//       document.getElementById('model_status').innerText = data.latest_raw_data
//         .result
//         ? '합격'
//         : '불합격';

//       // IPG 정보 업데이트
//       document.getElementById('ipg_program').innerText = data.weld_info.program;
//       document.getElementById('ipg_index').innerText = data.weld_info.id;
//       document.getElementById('ipg_power').innerText = data.weld_info.power;
//       document.getElementById('ipg_freq').innerText = data.weld_info.freq;
//       document.getElementById('ipg_length').innerText = data.weld_info.length;

//       // 금일생산량 업데이트
//       document.getElementById('total_ok_num').innerText = data.total_ok_count;
//       document.getElementById('total_ng_num').innerText = data.total_ng_count;

//       // 현재 모델 생산량 업데이트
//       document.getElementById('cur_ok_num').innerText =
//         data.current_model_ok_count;
//       document.getElementById('cur_ng_num').innerText =
//         data.current_model_ng_count;

//       // 조립비전 및 용접비전 업데이트
//       document.getElementById('before_v_total_num').innerText =
//         data.total_before_count;
//       document.getElementById('before_v_ok_num').innerText =
//         data.before_ok_count;
//       document.getElementById('before_v_ng_num').innerText =
//         data.before_ng_count;
//       document.getElementById('after_v_total_num').innerText =
//         data.total_after_count;
//       document.getElementById('after_v_ok_num').innerText = data.after_ok_count;
//       document.getElementById('after_v_ng_num').innerText = data.after_ng_count;
//     })
//     .catch((error) => console.error('Error fetching data:', error));
// }
