// ***********************************  Timer  ***********************************
const eventDate = new Date().getTime() + 1000 * 60 * 60;        // date of the Event we countdown - 1hr from refresh
// const exam_id = 
exam_id = document.getElementById('exam_id').value;
console.log(exam_id)
const timer = setInterval(() => {
    const actualTime = new Date().getTime();
    const difference = eventDate - actualTime;

    const minutes = difference % (1000 * 60 * 30) / (1000 * 60);
    const seconds = difference % (1000 * 60) / 1000;

    const minDozens = Math.floor(minutes / 10);
    const minUnity = Math.floor(minutes % 10);
    const secDozens = Math.floor(seconds / 10);
    const secUnity = Math.floor(seconds % 10);

    const hMinDozens = document.getElementById('min-dozens');
    const hMinUnits = document.getElementById('min-unity');
    const hSecDozens = document.getElementById('sec-dozens');
    const hSecUnits = document.getElementById('sec-unity');

    hMinDozens.innerHTML = minDozens;
    hMinUnits.innerHTML = minUnity;
    hSecDozens.innerHTML = secDozens;
    hSecUnits.innerHTML = secUnity;

    hMinDozens.classList.remove('timer-blur');
    hMinUnits.classList.remove('timer-blur');
    hSecDozens.classList.remove('timer-blur');
    hSecUnits.classList.remove('timer-blur');

    if(seconds % 1 < 0.3){
        hSecUnits.classList.add('timer-blur'); // second update
        if(secUnity == 0) {
            hSecDozens.classList.add('timer-blur');     // second dozens update
            if(secDozens == 0) {
                hMinUnits.classList.add('timer-blur');  // min update
                if(minUnity == 0) {
                    hMinDozens.classList.add('timer-blur'); // min dozens update
                    window.location.href = "http://127.0.0.1:8000/student/result/"+exam_id;
                    // window.location.href = "http://127.0.0.1:8000/student/exam-details";
                }
            }
        }
    }


    if(difference < 0){
        document.getElementById('message').innerHTML = "Thank you for nice time together 😄";

      hSecUnits.classList.remove('timer-blur');

        hMinDozens.innerHTML = 0;
        hMinUnits.innerHTML = 0;
        hSecDozens.innerHTML = 0;
        hSecUnits.innerHTML = 0;
        clearInterval(timer);
    }
}, 200);

//  ***********************************  page next and previous  ***********************************

    let currentPage = 1;
    const totalPages = 20;

    function showPage(action, pk) {
      const pages = document.querySelectorAll('.page');

      pages[currentPage - 1].classList.remove('active');

      if (action === 'prev') {
        currentPage = Math.max(currentPage - 1, 1);
      } else if (action === 'next') {

        console.log(pk)

        currentPage = Math.min(currentPage + 1, totalPages);
      }

      pages[currentPage - 1].classList.add('active');
    }

// ***********************************  Answer Submission  ***********************************
    function submitAnswer(a){
      j = document.getElementById("floatingTextarea_"+a).value

      $.ajax({
        type: 'get',
        url: '/student/answer_questions_in_exam/'+a,
        data: {'answer':j},
        success: function(response) {alert(response.msg)}
      })
    }
