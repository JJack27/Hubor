<template>
    <div>
        This is the dashboard page
    </div>
</template>

<script>
export default {
    name: "Dashboard",

    mounted(){
        
        // redirect user to the login page if the sessionid and csrtoken doesn't exist
        if(this.$getCookie('sessionid') === null
            && this.$getCookie('csrftoken') === null){
            this.$router.push('/');
        }else{
            // if currentUserInfo is empty but the session exists. Get from the server
            this.$get('api/myinfo/')
                .then((response) => {
                    // update user info in the store.
                    this.$store.dispatch('accounts/login', response.data);
                }).catch((error) =>{
                    // redirect it to the home page if getting error
                    console.log(error);
                    this.$router.push('/');
                })
        }
        
    }
}
</script>

<style >
    
</style>