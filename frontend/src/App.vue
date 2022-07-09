<template>
  <div class="container">
    <header>
      <div class="row">
        <div class="col-md-12">
          <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <router-link to="/" class="navbar-brand">Foodlist</router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbar">
              <ul class="navbar-nav">
                <li class="nav-item">
                  <router-link to="/list/consuming" class="nav-link">Consuming</router-link>
                </li>
                <li class="nav-item">
                  <router-link to="/list/shopping" class="nav-link">Shopping</router-link>
                </li>
                <li class="nav-item">
                  <router-link to="/list/editing" class="nav-link">Editing</router-link>
                </li>
              </ul>
            </div>
          </nav>
        </div>
      </div>
    </header>
    <main>
      <div class="row">
        <div class="col-md-12">
          <router-view></router-view>
        </div>
      </div>
    </main>
  </div>
</template>
