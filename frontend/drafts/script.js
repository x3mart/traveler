function showMenu(id){

    elem = document.getElementById(id); 

    state = elem.style.display; 
    
    if 
        (state =='none') elem.style.display='block';
        
    else 
        elem.style.display='none';
        
}