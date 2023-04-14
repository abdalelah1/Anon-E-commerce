var updateBtns=document.getElementsByClassName('update-card')
var viewProduct=document.getElementsByClassName('view-product');


for(var i =0;i<viewProduct.length;i++)
{
  viewProduct[i].addEventListener('click',function()
    {
      
      var  productId=this.dataset.product 
      var  action   =this.dataset.action
      console.log('prodcutid : ',productId,'action :',action)
      console.log('from update')
      console.log('user',user)
       view_product(productId,action)
    })
} 
for(var i =0;i<updateBtns.length;i++)

    updateBtns[i].addEventListener('click',function()
    {
      console.log('hiih')
      var  productId=this.dataset.product
      var  action   =this.dataset.action    
      console.log('prodcutid : ',productId,'action :',action)
      console.log('User',user)
      if (user === 'AnonymousUser')
      {
        console.log('not log in')
      }
      else{
        console.log('log in ')
        UpdateUserOrder(productId,action)

      }
    })


function UpdateUserOrder(prodcutid,action)
{
  console.log('user log in,sending data')
  var url ='/update_item/'
  fetch(url,{
    method:'POST',
    
    headers:{
    'Content-Type':'application/json',
    'X-CSRFToken':csrftoken,    
    },
    body:JSON.stringify({
      'prodcutid':prodcutid,
      'action':action,
    })
  })
  .then((response)=>{
    
    return response.json()
    
  })
  .then((data)=>{
    console.log('data',data)
   window.location.reload()
  })
}
function view_product(prodcutid,action)
{
  console.log("from view",prodcutid)
  var url ='/view_item/'
  
  fetch(url,{
    method:'POST',
    
    headers:{
    'Content-Type':'application/json',
    'X-CSRFToken':csrftoken,    
    },
    body:JSON.stringify({
      'prodcutid':prodcutid,
      'action':action,
    })
  })
  .then((response)=>{
    
    window.location.href = '/details/' + prodcutid+ '/';
    
  })
  .then((data)=>{
    console.log('data',data)
  })
}