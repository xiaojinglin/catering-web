window.addEventListener('load', (event) => {
    // form radio buttons interactions
    const radioCircles = document.getElementsByClassName('fa-check-circle');

    for (let i = 0; i < radioCircles.length; i++) {
        radioCircles[i].addEventListener('click', ()=>{
            (radioCircles[i].previousSibling.previousSibling.checked == true) ? radioCircles[i].previousSibling.previousSibling.checked = false : radioCircles[i].previousSibling.previousSibling.checked = true;
        });
    };
});