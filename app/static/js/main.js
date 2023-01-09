// Параллакс рук
new Rellax('.parellax', { horizontal: true });


//Появление рук
function onEntry(entry) {
    entry.forEach(change => {
      if (change.isIntersecting) {
       change.target.classList.add('element-show');
      }
    });
  }
  
  let options = {
    threshold: [0.5] };
  let observer = new IntersectionObserver(onEntry, options);
  let elements = document.querySelectorAll('.hand_1, .hand_2 ');
  
  for (let elm of elements) {
    observer.observe(elm);
  }