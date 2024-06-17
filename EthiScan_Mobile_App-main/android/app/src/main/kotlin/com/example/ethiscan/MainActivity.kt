package com.example.ethiscan

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.PixelFormat
import android.hardware.display.DisplayManager
import android.media.ImageReader
import android.media.projection.MediaProjection
import android.media.projection.MediaProjectionManager
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.provider.Settings
import android.util.DisplayMetrics
import android.view.Gravity
import android.view.LayoutInflater
import android.view.WindowManager
import android.widget.Button
import android.speech.tts.TextToSpeech
import java.util.*
import android.widget.Toast
import androidx.annotation.NonNull
import androidx.annotation.RequiresApi
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import java.io.ByteArrayOutputStream
import kotlinx.coroutines.*
import android.content.SharedPreferences


class MainActivity : FlutterActivity() {
    private val CHANNEL = "flutter.native/helper"
    private lateinit var overlayButton: Button
    private lateinit var mediaProjectionServiceIntent: Intent
    private lateinit var mediaProjectionManager: MediaProjectionManager
    private val PREF_NAME = "MyPreferences"
    private val KEY_COUNT = "count"
    private val INTRO_COUNT = "intro"

    private lateinit var sharedPreferences: SharedPreferences

    companion object {
        const val SCREEN_CAPTURE_REQUEST_CODE = 100
    }

    @ExperimentalStdlibApi
    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        sharedPreferences = getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                when {
                    call.method == "changeColor" -> {
                        showOverlayButton()
                    }
                    call.method == "StopOverlay" -> {
                    stopOverlay()
                    }
                    call.method == "ShowToast" -> {
                    stopOverlay()
                    }
                    call.method == "getCount" -> {
                    val count = sharedPreferences.getInt(KEY_COUNT, 0)
                    result.success(count)
                    }
                    call.method == "incrementCount" -> {
                        val count = sharedPreferences.getInt(KEY_COUNT, 0) + 1
                        with(sharedPreferences.edit()) {
                            putInt(KEY_COUNT, count)
                            apply()
                        }
                        result.success(count)
                    }
                    call.method == "GetIntro" -> {
                    val INTRO_COUNTS = sharedPreferences.getInt(INTRO_COUNT, 0)
                    result.success(INTRO_COUNTS)
                    }
                    call.method == "RemoveIntro" -> {
                        val INTRO_COUNTS = sharedPreferences.getInt(INTRO_COUNT, 0) + 1
                        with(sharedPreferences.edit()) {
                            putInt(INTRO_COUNT, INTRO_COUNTS)
                            apply()
                        }
                        result.success(INTRO_COUNTS)
                    }
                    call.method == "speak"->{
                        val text = call.argument<String>("text")
                        if (text != null) {
                            speak(text)
                            result.success(null)
                        } else {
                            result.error("TEXT_NULL", "Text cannot be null", null)
                        }
                    }
                    else -> {
                        result.notImplemented()
                    }
                }
            }
    }
     private lateinit var textToSpeech: TextToSpeech

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        textToSpeech = TextToSpeech(this) { status ->
            if (status != TextToSpeech.ERROR) {
                textToSpeech.language = Locale.US
            }
        }
    }

    private fun speak(text: String) {
        textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
    }

private fun ShowToast() {
   Toast.makeText(
                this,
                "Result Has Arrived In App.",
                Toast.LENGTH_SHORT
            ).show()
}


private fun stopOverlay() {
    if (::overlayButton.isInitialized) {
        val windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        windowManager.removeView(overlayButton)
    }

    if (::mediaProjectionServiceIntent.isInitialized) {
        stopService(mediaProjectionServiceIntent)
    }
}

private fun showOverlayButton() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
        // Ask for permission to draw overlays
        val intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
        startActivity(intent)
    } else {
        // Initialize the MediaProjectionManager
        mediaProjectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager

        // Start the foreground service
        startForegroundService()

        // Create overlay button
        val windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        val layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        )

        layoutParams.gravity = Gravity.CENTER or Gravity.START
        overlayButton = LayoutInflater.from(this).inflate(R.layout.overlay_button, null) as Button

        overlayButton.setOnClickListener {
            // Handle button click
            // You can perform any action when the overlay button is clicked
            
            captureScreenshotAndSave()
        }

        windowManager.addView(overlayButton, layoutParams)
    }
}


    private fun startForegroundService() {
        mediaProjectionServiceIntent = Intent(this, MediaProjectionService::class.java)
        startService(mediaProjectionServiceIntent)
    }

    private fun captureScreenshotAndSave() {
        // Check for the necessary permission
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            startActivityForResult(
                mediaProjectionManager.createScreenCaptureIntent(),
                SCREEN_CAPTURE_REQUEST_CODE
            )
        } else {
            // Handle the case where the API level is not sufficient for screen capture
            Toast.makeText(
                this,
                "Screen capture not supported on this device",
                Toast.LENGTH_SHORT
            ).show()
        }
    }

@RequiresApi(Build.VERSION_CODES.LOLLIPOP)
override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
    if (requestCode == SCREEN_CAPTURE_REQUEST_CODE) {
        if (resultCode == RESULT_OK && data != null) {
            Toast.makeText(this, "Move To The Portion You Want To Check", Toast.LENGTH_SHORT).show()
            val mediaProjection = mediaProjectionManager.getMediaProjection(resultCode, data)
            val screenshot = captureScreenshot(mediaProjection)
            sendScreenshotToFlutter(screenshot)
            val savedImagePath= saveScreenshotToGallery(screenshot)
            if (savedImagePath != null) {
                Toast.makeText(this, "Result Will Be Displayed In App.", Toast.LENGTH_SHORT).show()
            } 
            else 
            {
                Toast.makeText(this, "Failed to save screenshot", Toast.LENGTH_SHORT).show()
            }
        } else {
            Toast.makeText(this, "Permission not granted", Toast.LENGTH_SHORT).show()
        }
    }
}

private fun sendScreenshotToFlutter(bitmap: Bitmap) {
    val stream = ByteArrayOutputStream()
    bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
    val byteArray = stream.toByteArray()

    MethodChannel(flutterEngine?.dartExecutor?.binaryMessenger!!, CHANNEL)
        .invokeMethod("onScreenshotReceived", byteArray)
}


   @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
private fun captureScreenshot(mediaProjection: MediaProjection): Bitmap {
    val displayMetrics = DisplayMetrics()
    windowManager.defaultDisplay.getMetrics(displayMetrics)
    val width = displayMetrics.widthPixels
    val height = displayMetrics.heightPixels
    val imageReader = ImageReader.newInstance(width, height, PixelFormat.RGBA_8888, 2)

    val virtualDisplay = mediaProjection.createVirtualDisplay(
        "ScreenCapture",
        width,
        height,
        displayMetrics.densityDpi,
        DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
        imageReader.surface,
        null,
        null
    )
    // Delay to allow time for the image to be rendered on the virtual display
    Thread.sleep(3000)
    val image = imageReader.acquireLatestImage()

    if (image != null) {
        try {
            val planes = image.planes
            val buffer = planes[0].buffer
            val pixelStride = planes[0].pixelStride
            val rowStride = planes[0].rowStride
            val rowPadding = rowStride - pixelStride * width

            val bitmap = Bitmap.createBitmap(
                width + rowPadding / pixelStride,
                height,
                Bitmap.Config.ARGB_8888
            )
            bitmap.copyPixelsFromBuffer(buffer)

            return bitmap
        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            image.close()
            virtualDisplay.release()
            mediaProjection.stop()
        }
    }

    return Bitmap.createBitmap(1, 1, Bitmap.Config.ARGB_8888)
}


    private fun saveScreenshotToGallery(bitmap: Bitmap): String? {
        val savedImageUri = MediaStore.Images.Media.insertImage(
            contentResolver,
            bitmap,
            "Screenshot_${System.currentTimeMillis()}",
            "Screenshot taken by the app"
        )

        return savedImageUri?.toString()
    }
}

