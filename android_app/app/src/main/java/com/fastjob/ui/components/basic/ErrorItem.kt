package com.fastjob.ui.components.basic

import android.content.res.Configuration
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.theme.FastjobTheme

/**
 * Componente que muestra un mensaje de error con un icono
 * @param text Texto a mostrar
 */
@Composable
fun ErrorItem(
    text: String = stringResource(id = R.string.default_error)
) {
    // columna con el icono y el texto
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp),
        modifier = Modifier
            .fillMaxWidth()
            .padding(6.dp)
    ) {
        // icono de error
        Icon(
            painter = painterResource(id = R.drawable.error),
            contentDescription = stringResource(id = R.string.error_icon_description),
            tint = colorScheme.error,
        )
        // texto de error
        Text(
            text = text,
            textAlign = TextAlign.Center
        )
    }
}

@Preview(showBackground = true)
@Composable
fun ErrorItemPreview() {
    FastjobTheme {
        ErrorItem()
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun ErrorItemPreviewDark() {
    FastjobTheme {
        ErrorItem()
    }
}