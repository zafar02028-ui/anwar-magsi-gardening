document.addEventListener('DOMContentLoaded',function(){
  // Mobile nav toggle
  const toggle=document.querySelector('.nav-toggle');
  const navList=document.getElementById('nav-list');
  toggle&&toggle.addEventListener('click',()=>{
    const expanded=toggle.getAttribute('aria-expanded')==='true';
    toggle.setAttribute('aria-expanded',!expanded);
    navList.style.display = expanded ? 'none' : 'flex';
  });

  // Floating WhatsApp
  const wa=document.getElementById('whatsappFloat');
  wa&&wa.addEventListener('click',()=>{window.open('https://wa.me/971553433607','_blank')});

  // Gallery lightbox
  const items=Array.from(document.querySelectorAll('.gallery-item'));
  const lb=document.getElementById('lightbox');
  const lbImg=document.getElementById('lightboxImg');
  let idx=-1;
  function openLB(i){
    idx=i;lbImg.src=items[i].dataset.src;lb.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';
  }
  function closeLB(){lb.setAttribute('aria-hidden','true');lbImg.src='';document.body.style.overflow='';}
  items.forEach((it,i)=>it.addEventListener('click',()=>openLB(i)));
  document.querySelector('.lb-close')?.addEventListener('click',closeLB);
  document.querySelector('.lb-next')?.addEventListener('click',()=>{if(idx<items.length-1)openLB(idx+1)});
  document.querySelector('.lb-prev')?.addEventListener('click',()=>{if(idx>0)openLB(idx-1)});
  lb.addEventListener('click',(e)=>{if(e.target===lb)closeLB();});

  // Simple contact handler (no backend) — opens WhatsApp prefilled message
  window.handleContact=function(e){
    e.preventDefault();
    const f=new FormData(e.target);
    const name=f.get('name')||'';
    const phone=f.get('phone')||'';
    const service=f.get('service')||'';
    const msg=f.get('message')||'';
    const text=`Hi, I am ${name}. Phone: ${phone}. Service: ${service}. Message: ${msg}`;
    const url='https://wa.me/971553433607?text='+encodeURIComponent(text);
    window.open(url,'_blank');
  };
});
