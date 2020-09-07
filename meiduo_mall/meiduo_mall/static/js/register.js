let  vm = new Vue({
   el:"#app",
     // 修改Vue读取变量的语法
   delimiters: ['[[', ']]'],
   data:{
       username:'',
       password:'',
       password2:'',
       mobile:'',
       allow:'',
       image_code_url:'',
       uuid:'',
       image_code:'',
       sms_code_tip:'获取短信验证码',



       error_name:false,
       error_password:false,
       error_password2:false,
       error_mobile:false,
       error_allow:false,
       error_image_code:false,

       error_name_message:'',
       error_mobile_message:'',
       error_image_code_message:'',

   },
    mounted(){//页面加载完会调用的
       this.generate_image_code()
    },
    methods:{
    generate_image_code(){
        this.uuid = generateUUID();
        this.image_code_url = '/image_code/'+ this.uuid +'/';
    },
    check_username(){
         let re = /^[a-zA-Z0-9]{5,20}$/;
         if (re.test(this.username)){
             this.error_name = false;
         }else {
             this.error_name_message = '请输入5-20个字符的用户名';
             this.error_name = true;
         }
         if (this.error_name == false){
             let  url = '/usernames/' + this.username + '/count/';
             axios.get(url,{
                 responseType: 'json'
             })
                 .then(response =>{
                     if (response.data.count == 1) {
                            // 用户名已存在
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            // 用户名不存在
                            this.error_name = false;
                        }
                 })
                 .catch(error => {
                        console.log(error.response);
                    })
         }
    },
    // 校验密码
    check_password() {
        let re = /^[0-9A-Za-z]{8,20}$/;
        if (re.test(this.password)) {
            this.error_password = false;
        } else {
            this.error_password = true;
        }
    },
    // 校验确认密码
    check_password2() {
        if (this.password != this.password2) {
            this.error_password2 = true;
        } else {
            this.error_password2 = false;
        }
    },
    // 校验手机号
    check_mobile() {
        let re = /^1[3-9]\d{9}$/;
        if (re.test(this.mobile)) {
            this.error_mobile = false;
        } else {
            this.error_mobile_message = '您输入的手机号格式不正确';
            this.error_mobile = true;
        }
    },
    check_image_code(){
      if (this.image_code.length != 4){
          this.error_image_code = true
          this.error_image_code_message = '请输入图形验证码'
      }else  {
          this.error_image_code = false
      }
    },
    send_sms_code(){
        let url = '/sms_codes/'+this.mobile+'/?image_code='+this.image_code+'&uuid='+this.uuid
        axios.get(url,{
            responseType: 'json'
        })
            .then(response=>{
                if (response.data.code == '0'){
                    let num = 60;
                    let t = setInterval(()=>{
                        if (num == 1){
                            clearInterval(t);
                            this.sms_code_tip = '获取短信验证码';
                            this.generate_image_code();
                        }else {
                          num -= 1;
                        this.sms_code_tip = num + '秒';
                        }

                    },1000)
                }else {
                    if (response.data.code == '4001'){
                        this.error_image_code_message = "response.data.errmsg";
                        this.error_image_code = true;
                    }
                }
            })
            .catch(error=>{
                console.log(error.response)
            })
    },
    // 校验是否勾选协议
    check_allow() {
        if (!this.allow) {
            this.error_allow = true;
        } else {
            this.error_allow = false;
        }
    },
    // 监听表单提交事件
    on_submit() {
        this.check_username();
        this.check_password();
        this.check_password2();
        this.check_mobile();
        this.check_allow();

        // 在校验之后，注册数据中，只要有错误，就禁用掉表单的提交事件
        if (this.error_name == true || this.error_password == true || this.error_password2 == true || this.error_mobile == true || this.error_allow == true) {
            // 禁用掉表单的提交事件
            window.event.returnValue = false;
        }
    },
   }
});