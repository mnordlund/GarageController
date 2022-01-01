package se.mnordlund.garagecontroller

import android.Manifest
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationRequest
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
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
import java.text.DecimalFormat


class MainActivity : AppCompatActivity() {

    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var doorHandler: DoorHandler


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        doorHandler = DoorHandler(this, applicationContext)

    }

    fun onTestButton(view: View) {
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
                var door = Location("")
                door.latitude = 56.906803
                door.longitude = 12.509708

                var distance = location.distanceTo(garage)
                var builder = AlertDialog.Builder(this)

                builder.setTitle("Location")
                builder.setMessage(
                    location.toString() + garage.toString() + "Distance: " + distance
                )
                builder.setPositiveButton(android.R.string.ok) { _, _ ->
                    Toast.makeText(
                        applicationContext,
                        "I'll do it",
                        Toast.LENGTH_SHORT
                    ).show()
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
                if(distance < 10) {
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

    fun onDoIt(view: View) {
        checkDistanceFromGarage()
    }
}