 // Get the scroller element 
 var scroller = document.querySelector('.scroller'); 
 // Get the content that will be scrolled 
 var scrollerContent = scroller.querySelector('div'); 
 // Get the total height of the scroller content 
 var scrollerHeight = scrollerContent.getBoundingClientRect().height; 
 // Get the height of the scroller 
 var scrollerViewHeight = scroller.getBoundingClientRect().height; 
 // Get the total scrollable height 
 var scrollableHeight = scrollerHeight - scrollerViewHeight; 
 // Set the initial scroll position to 0 
 scroller.scrollTop = 0; 
 // Animate the scroll position 
 function animateScroll() { 
    // Calculate the new scroll position 
    var scrollPosition = scroller.scrollTop + 1; 
    // If we've reached the bottom, reset to the top 
    if (scrollPosition >= scrollableHeight) { scrollPosition = 0; } 
    // Update the scroll position 
    scroller.scrollTop = scrollPosition; 
    // Animate again 
    requestAnimationFrame(animateScroll); } 
    // Start the animation 
    animateScroll();