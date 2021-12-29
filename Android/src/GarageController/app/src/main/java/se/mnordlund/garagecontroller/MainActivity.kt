package se.mnordlund.garagecontroller

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Toast
import com.google.firebase.database.FirebaseDatabase

class MainActivity : AppCompatActivity() {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    fun onDoIt(view : View) {
        val cmds = FirebaseDatabase.getInstance(BuildConfig.DB_URL).getReference("commands")
        cmds.child("operate").setValue(true)
    }
}