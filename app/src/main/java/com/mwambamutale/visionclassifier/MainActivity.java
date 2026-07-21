package com.mwambamutale.visionclassifier;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.media.ThumbnailUtils;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

import com.mwambamutale.visionclassifier.ml.Model;


public class MainActivity extends AppCompatActivity {

    Button camera, gallery;
    ImageView imageView;
    TextView result;
    private static final String TAG = "MwambaVision";
    private static final String[] CLASSES = {"Apple", "Banana", "Orange"};
    private static final int IMAGE_SIZE = 32;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        camera = findViewById(R.id.button);
        gallery = findViewById(R.id.button2);

        result = findViewById(R.id.result);
        imageView = findViewById(R.id.imageView);

        camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(cameraIntent, 3);
                } else {
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, 100);
                }
            }
        });
        gallery.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent cameraIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                startActivityForResult(cameraIntent, 1);
            }
        });
    }

    public void classifyImage(Bitmap image){
        if (image == null) {
            showError("No image selected. Try again.");
            return;
        }

        Model model = null;
        try {
            model = Model.newInstance(getApplicationContext());

            // Creates inputs for reference.
            TensorBuffer inputFeature0 = TensorBuffer.createFixedSize(new int[]{1, 32, 32, 3}, DataType.FLOAT32);
            ByteBuffer byteBuffer = ByteBuffer.allocateDirect(4 * IMAGE_SIZE * IMAGE_SIZE * 3);
            byteBuffer.order(ByteOrder.nativeOrder());

            int[] intValues = new int[IMAGE_SIZE * IMAGE_SIZE];
            image.getPixels(intValues, 0, image.getWidth(), 0, 0, image.getWidth(), image.getHeight());
            int pixel = 0;
            for(int i = 0; i < IMAGE_SIZE; i ++){
                for(int j = 0; j < IMAGE_SIZE; j++){
                    int val = intValues[pixel++]; // RGB
                    byteBuffer.putFloat((val >> 16) & 0xFF);
                    byteBuffer.putFloat((val >> 8) & 0xFF);
                    byteBuffer.putFloat(val & 0xFF);
                }
            }

            inputFeature0.loadBuffer(byteBuffer);

            // Runs model inference and gets result.
            Model.Outputs outputs = model.process(inputFeature0);
            TensorBuffer outputFeature0 = outputs.getOutputFeature0AsTensorBuffer();

            float[] confidences = outputFeature0.getFloatArray();
            // find the index of the class with the biggest confidence.
            int maxPos = 0;
            float maxConfidence = 0;
            for (int i = 0; i < confidences.length; i++) {
                if (confidences[i] > maxConfidence) {
                    maxConfidence = confidences[i];
                    maxPos = i;
                }
            }
            if (maxPos < CLASSES.length) {
                result.setText(CLASSES[maxPos]);
            } else {
                showError("The model returned an unknown class.");
            }

        } catch (Exception e) {
            Log.e(TAG, "Image classification failed", e);
            showError("Could not run image classification.");
        } finally {
            if (model != null) {
                model.close();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if(resultCode == RESULT_OK && data != null){
            if(requestCode == 3){
                if (data.getExtras() == null || data.getExtras().get("data") == null) {
                    showError("Camera did not return an image.");
                    super.onActivityResult(requestCode, resultCode, data);
                    return;
                }

                Bitmap image = (Bitmap) data.getExtras().get("data");
                int dimension = Math.min(image.getWidth(), image.getHeight());
                image = ThumbnailUtils.extractThumbnail(image, dimension, dimension);
                imageView.setImageBitmap(image);

                image = Bitmap.createScaledBitmap(image, IMAGE_SIZE, IMAGE_SIZE, false);
                classifyImage(image);
            }else{
                Uri dat = data.getData();
                if (dat == null) {
                    showError("Gallery did not return an image.");
                    super.onActivityResult(requestCode, resultCode, data);
                    return;
                }

                Bitmap image = null;
                try {
                    image = MediaStore.Images.Media.getBitmap(this.getContentResolver(), dat);
                } catch (IOException e) {
                    Log.e(TAG, "Could not load gallery image", e);
                    showError("Could not load the selected image.");
                }

                if (image != null) {
                    imageView.setImageBitmap(image);
                    image = Bitmap.createScaledBitmap(image, IMAGE_SIZE, IMAGE_SIZE, false);
                    classifyImage(image);
                }
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    private void showError(String message) {
        result.setText(message);
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
}
