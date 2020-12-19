<template>
    <div>
        <!--Hey! This is the original version of Simple CSS Waves-->

        <div class="header">

            <!--Content before waves-->
            <div class="inner-header flex">
                <a-row>
                  <a-col :span="24">
                    <h1 id='header'> Vital Sign Project </h1>
                  </a-col>
                </a-row>
                
                <a-row type="flex" justify="center">
                  <a-col :span="16" >
                    <login-card id='login-card'/>
                  </a-col>
                </a-row>
            </div>

            <!--Waves Container-->
            <div>
                <svg
                    class="waves"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    viewBox="0 24 150 28"
                    preserveAspectRatio="none"
                    shape-rendering="auto">
                    <defs>
                        <path
                            id="gentle-wave"
                            d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z"/>
                    </defs>
                    <g class="parallax">
                        <use xlink:href="#gentle-wave" x="48" y="0" fill="rgba(255,255,255,0.7"/>
                        <use xlink:href="#gentle-wave" x="48" y="3" fill="rgba(255,255,255,0.5)"/>
                        <use xlink:href="#gentle-wave" x="48" y="5" fill="rgba(255,255,255,0.3)"/>
                        <use xlink:href="#gentle-wave" x="48" y="7" fill="#fff"/>
                    </g>
                </svg>
            </div>
            <!--Waves end-->



        </div>
        <!--Header ends-->

        <!--Content starts
        <div class="content flex">
          <p>Daniel Österman | 2019 | Free to use</p>
        </div>
        -->
    </div>

</template>

<style>

.header {
    position: relative;
    text-align: center;
    background: linear-gradient(60deg, #7973df 0%, #b87edf 100%);
    color: white;
}


.inner-header {
    height: 65vh;
    width: 100%;
    margin: 0;
    padding: 0;
}

.flex {
    /*Flexbox for containers*/
    justify-content: center;
    align-items: center;
    text-align: center;
}

.waves {
    position: relative;
    width: 100%;
    height: 15vh;
    margin-bottom: -7px;
    /*Fix for safari gap*/
    min-height: 55px;
    max-height: 150px;
}

.content {
    position: relative;
    height: 10vh;
    text-align: center;
    background-color: white;
}

/* Animation */

.parallax > use {
    animation: move-forever 25s cubic-bezier(.55,.5,.45,.5) infinite;
}
.parallax > use:nth-child(1) {
    animation-delay: -2s;
    animation-duration: 7s;
}
.parallax > use:nth-child(2) {
    animation-delay: -3s;
    animation-duration: 10s;
}
.parallax > use:nth-child(3) {
    animation-delay: -4s;
    animation-duration: 13s;
}
.parallax > use:nth-child(4) {
    animation-delay: -5s;
    animation-duration: 20s;
}
@keyframes move-forever {
    0% {
        transform: translate3d(-90px,0,0);
    }
    100% {
        transform: translate3d(85px,0,0);
    }
}
/*Shrinking for mobile*/
@media (max-width: 768px) {
    .waves {
        height: 40px;
        min-height: 40px;
    }
    .content {
        height: 30vh;
    }
    h1 {
        font-size: 24px;
    }
}

#header{
  margin-top:100pt;
  font-size: 40pt;
  color: #FFFFFF;
  font-family: 'Bungee', cursive;
}

#login-card{
  width: 100%;
  
}
</style>

<script>
import LoginCard from '@/components/LoginCard'

export default {
  name: "Home", 
  components: {
      LoginCard
    }
  };
</script>