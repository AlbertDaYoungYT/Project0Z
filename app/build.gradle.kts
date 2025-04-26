plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    kotlin("plugin.serialization") version "1.9.21" // or latest version
}

android {
    namespace = "com.abot.project0z"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.abot.project0z"
        minSdk = 31
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
    buildFeatures {
        compose = true
    }
    android { packagingOptions { resources.excludes.add("META-INF/*") } }
}

dependencies {
    implementation("androidx.compose.ui:ui:1.7.8")
    implementation(libs.androidx.animation.android)
    implementation(libs.androidx.animation.android)
    implementation(libs.androidx.animation.android)
    implementation(libs.androidx.foundation.android)
    implementation(libs.androidx.benchmark.common)
    implementation(libs.ui)
    implementation(libs.gson)
    implementation(libs.material)
    implementation(libs.androidx.datastore.preferences)
    implementation(libs.kotlinx.serialization.json)
    val nav_version = "2.8.9"

    implementation("org.slf4j:slf4j-api:2.0.12")
    // Add your chosen logging implementation here, e.g.:
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4") // Or latest version
    // Jetpack Compose integration
    implementation("androidx.navigation:navigation-compose:$nav_version")

    implementation("org.bouncycastle:bcprov-jdk15on:1.70")

    implementation("androidx.datastore:datastore-preferences:1.0.0")

    // Reflections libraries.
    implementation(libs.reflections)
    implementation(libs.reflectasm)
    implementation(libs.rtree.multi)

    // Views/Fragments integration
    implementation("androidx.navigation:navigation-fragment:$nav_version")
    implementation("androidx.navigation:navigation-ui:$nav_version")

    // Feature module support for Fragments
    implementation("androidx.navigation:navigation-dynamic-features-fragment:$nav_version")

    // Testing Navigation
    androidTestImplementation("androidx.navigation:navigation-testing:$nav_version")

    // JSON serialization library, works with the Kotlin serialization plugin
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")

    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.ui.test.junit4)
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest)
}