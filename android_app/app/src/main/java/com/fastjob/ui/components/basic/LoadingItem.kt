package com.fastjob.ui.components.basic

import android.content.res.Configuration
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.theme.FastjobTheme

/**
 * Componente que muestra un [CircularProgressIndicator] y un [Text] con un mensaje.
 * Se usa para indicar que se está cargando información.
 * @param text Mensaje que se muestra junto al [CircularProgressIndicator].
 */
@Composable
fun LoadingItem(
    text: String = stringResource(id = R.string.default_loading)
) {
    // Columna que contiene el CircularProgressIndicator y el Text.
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp),
        modifier = Modifier
            .fillMaxWidth()
            .padding(6.dp)
    ) {
        // CircularProgressIndicator con el color primario de la app.
        CircularProgressIndicator(
            modifier = Modifier.size(50.dp),
            color = colorScheme.primary
        )
        // Text con el mensaje.
        Text(
            text = text
        )
    }
}

@Preview(showBackground = true)
@Composable
fun LoadingItemPreview() {
    FastjobTheme {
        LoadingItem()
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun LoadingItemPreviewDark() {
    FastjobTheme {
        LoadingItem()
    }
}