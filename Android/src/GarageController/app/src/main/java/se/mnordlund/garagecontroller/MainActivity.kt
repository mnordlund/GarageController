package se.mnordlund.garagecontroller

import android.Manifest
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationRequest
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Switch
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.tasks.CancellationTokenSource
import kotlin.math.acos
import kotlin.math.cos
import kotlin.math.sin
import com.google.android.gms.location.LocationResult
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import java.text.DecimalFormat


class MainActivity : AppCompatActivity() {

    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var doorHandler: DoorHandler
    private lateinit var isDoorOpenSwitch: Switch
    private lateinit var isDoorClosedSwitch: Switch
    private lateinit var isCarInGarage: Switch
    private lateinit var isLocked: Switch


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        doorHandler = DoorHandler(this, applicationContext)

        isDoorOpenSwitch = findViewById<Switch>(R.id.Opened)
        isDoorClosedSwitch = findViewById<Switch>(R.id.Closed)
        isCarInGarage = findViewById<Switch>(R.id.CarInGarage)
        isLocked = findViewById<Switch>(R.id.lock)

        setupListeners()



    }

    fun setupListeners() {
        var status = FirebaseDatabase.getInstance(BuildConfig.DB_URL).getReference("status")

        val statusListener = object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                isDoorOpenSwitch.isChecked = snapshot.child("doorOpened").value as Boolean
                isDoorClosedSwitch.isChecked = snapshot.child("doorClosed").value as Boolean
                isCarInGarage.isChecked = snapshot.child("carInGarage").value as Boolean
                isLocked.isChecked = snapshot.child("locked").value as Boolean
            }

            override fun onCancelled(error: DatabaseError) {
                Toast.makeText(
                    applicationContext,
                    "Failed to read status",
                    Toast.LENGTH_SHORT
                ).show()

                Log.w("gc", "load status cancelled", error.toException())
            }
        }

        status.addValueEventListener(statusListener)

    }

    fun checkPermissionForLocation(): Boolean{
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this@MainActivity,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(this@MainActivity,
                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), 1)
            } else {
                ActivityCompat.requestPermissions(this@MainActivity,
                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), 1)
            }
        }

        return (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED)
    }

    fun checkDistanceFromGarage(){
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this@MainActivity,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(this@MainActivity,
                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), 1)
            } else {
                ActivityCompat.requestPermissions(this@MainActivity,
                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), 1)
            }
            return
        }

        fusedLocationClient.lastLocation.addOnSuccessListener { location: Location?  ->
            if(location != null) {
                var garage = Location("")
                garage.latitude = BuildConfig.LAT
                garage.longitude = BuildConfig.LONG

                var distance =location.distanceTo(garage)

                // If we are too far away confirm opening the door
                if(distance < 20) {
                    doorHandler.operateDoor()
                }else {
                    var builder = AlertDialog.Builder(this)

                    builder.setTitle("Location")
                    builder.setMessage(
                        "Du är ${DecimalFormat("#.#").format(distance)} meter från garaget, vill du ändå öppna det?"
                    )
                    builder.setPositiveButton(android.R.string.ok) { _, _ ->
                        doorHandler.operateDoor()
                    }
                    builder.setNegativeButton(android.R.string.cancel) { _, _ ->
                        Toast.makeText(
                            applicationContext,
                            "Nehepp!",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                    builder.show()
                }
            }
        }
    }

    fun onLock(view: View) {
        doorHandler.lock(isLocked.isChecked)
    }

    fun onDoIt(view: View) {
        if(!isLocked.isChecked) {
            checkDistanceFromGarage()
        } else {
            Toast.makeText(applicationContext, "Dörren är låst", Toast.LENGTH_SHORT).show()
        }
    }
}