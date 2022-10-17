<template>
  <div id="app">
    <div id="nav">
      <div style="padding-left: 9%">
        <router-link to="/">Inicio</router-link> |
        <router-link to="/about">Nosotros</router-link>
      </div>
    </div>
    <div id="routerView">
      <router-view/>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding-bottom: 2%;
  padding-top: 2%;
  background-color: #7DDBF0;
  width: 100%;
  display: inline-block;
  text-align: left;
}

#nav a {
  font-size: 2vw;
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
#routerView
{
  margin-top: 1%;
}
</style>
