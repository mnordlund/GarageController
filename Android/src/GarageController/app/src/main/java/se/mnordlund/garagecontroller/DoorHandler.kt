package se.mnordlund.garagecontroller

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.core.app.ActivityCompat
import com.google.firebase.database.FirebaseDatabase

class DoorHandler(private var main: MainActivity, private var appContext: Context) {

    fun operateDoor() {
        val cmds = FirebaseDatabase.getInstance(BuildConfig.DB_URL).getReference("commands")
        cmds.child("operate").setValue(true)
        Toast.makeText(appContext, "Operating door", Toast.LENGTH_SHORT).show()
    }

    fun lock(lock: Boolean) {
        val cmds = FirebaseDatabase.getInstance(BuildConfig.DB_URL).getReference("commands")
        cmds.child("lock").setValue(lock)
        var message = if(lock) {
            "Låser"
        } else {
            "Låser upp"
        }

        Toast.makeText(appContext, message, Toast.LENGTH_SHORT).show()
    }

}