<template>
  <a-row>
    <a-col :span="24">
      <p id='header'> Vital Sign Project </p>
    </a-col>
  </a-row>
  <a-row>
    <a-col :span="24">
      <login-card/>
    </a-col>
  </a-row>
  <!-- 
    body {
  height:100vh;
  margin:0;
  background-image:radial-gradient(at top left,#766ff7 36%,#918de0 67%, transparent 60%);
  background-size:150% 100%;
  background-repeat:no-repeat;
}
  -->
</template>

<style >



.ant-card{
  width: 250pt;
  margin-left: auto;
  margin-right: auto;
}

#header{
  margin-top:50pt;
  font-size: 40pt;
  color: #FFFFFF;
}
</style>


<script>
import LoginCard from '@/components/LoginCard'

export default {
  name:"Home",
  components: { LoginCard },
  
};
</script>
