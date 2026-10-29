plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

val runNumber = System.getenv("GITHUB_RUN_NUMBER")?.toIntOrNull() ?: 1
// The release line ("0.2" while testing, "1.0" at launch) lives in version.txt so the app and the release tag always agree.
val versionLine = rootProject.file("version.txt").readText().trim()

android {
    namespace = "org.manahakku.app"
    compileSdk = 36

    defaultConfig {
        applicationId = "org.manahakku.app"
        minSdk = 26
        targetSdk = 36
        versionCode = 100 + runNumber   // continues after the last 0.1.x builds
        versionName = "$versionLine.$runNumber"
    }

    // Shared test key so each new build installs over the previous one.
    // Replace with a private key (kept in GitHub Secrets) before any Play Store release.
    signingConfigs {
        create("shared") {
            storeFile = file("mana-hakku-debug.keystore")
            storePassword = "android"
            keyAlias = "androiddebugkey"
            keyPassword = "android"
        }
        // Private release key: the build writes it from the GitHub Secrets MH_KEYSTORE_B64 / MH_KEYSTORE_PASS.
        // It is never stored in the repository. Without those secrets the shared test key is used.
        if (file("release.keystore").exists() && !System.getenv("MH_KEYSTORE_PASS").isNullOrEmpty()) {
            create("private") {
                storeFile = file("release.keystore")
                storePassword = System.getenv("MH_KEYSTORE_PASS")
                keyAlias = "manahakku"
                keyPassword = System.getenv("MH_KEYSTORE_PASS")
            }
        }
    }

    buildTypes {
        getByName("debug") {
            signingConfig = signingConfigs.getByName("shared")
        }
        getByName("release") {
            isMinifyEnabled = false
            signingConfig = signingConfigs.findByName("private") ?: signingConfigs.getByName("shared")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    lint {
        abortOnError = false
        checkReleaseBuilds = false
    }
}
